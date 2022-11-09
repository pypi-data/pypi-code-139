import getopt
import sys

import pandas as pd


def bed_artificial(input_bed):
    """
    from the initial bed, filter and return df with only oligos in chr_art
    """
    bed = pd.read_csv(input_bed, sep='\t', header=None)
    for k in range(len(bed)):
        if bed[0][k] != 'chr_art' or 'flank' in bed[3][k]:
            bed.drop([k], inplace=True)
    bed.reset_index(drop=True, inplace=True)
    return bed


def bed_genome(input_bed):
    """
    from the initial bed, filter and return df with only oligos in genome chromosomes
    """
    bed = pd.read_csv(input_bed, sep='\t', header=None)
    for k in range(len(bed)):
        if bed[0][k] == 'chr_art' or 'flank' in bed[3][k]:
            bed.drop([k], inplace=True)
    bed.reset_index(drop=True, inplace=True)
    return bed


# def cut_chr_art(input_oligos, input_bed):
# # not used
#     oligos = oligos_correction(input_oligos)
#     bed_art = bed_artificial(input_bed)
#     bed_gen = bed_genome(input_bed)
#     if len(bed_art) != len(bed_gen):
#         print("Error: there is a problem in the bed file (not same number of coordinates in genome and chr_art")
#         pass
#
#     for k in range(len(bed_art)):
#         start_art, end_art = bed_art[1][k], bed_art[1][k]
#         start_gen, end_gen = bed_gen[1][k], bed_gen[1][k]
#         start_capt, end_capt = oligos['start'][k], oligos['end'][k]
#
#         new_start = start_art + start_capt - start_gen
#         new_end = end_art + end_capt - end_gen
#
#         df = pd.DataFrame([['chr_art', new_start, new_end, oligos['type'][k], oligos['name'][k], '']],
#                           columns=['chr', 'start', 'end', 'type', 'name', 'sequence'])
#
#         oligos = pd.concat([oligos, df])
#         print(new_end - new_start == end_capt - start_capt)
#     return oligos


def oligos_correction(oligos_path):
    oligos = pd.read_csv(oligos_path, sep=",")
    oligos.columns = [oligos.columns[i].lower() for i in range(len(oligos.columns))]
    oligos.sort_values(by=['chr', 'start'], inplace=True)
    oligos.reset_index(drop=True, inplace=True)

    return oligos


def fragments_correction(fragments_path):
    fragments = pd.read_csv(fragments_path, sep='\t')
    fragments = pd.DataFrame({'frag': [k for k in range(len(fragments))],
                              'chr': fragments['chrom'],
                              'start': fragments['start_pos'],
                              'end': fragments['end_pos'],
                              'size': fragments['size'],
                              'gc_content': fragments['gc_content']
                              })

    return fragments


def starts_match(fragments, oligos_path):
    """
    If the capture oligos is inside a fragment, it changes the start of
    the oligos dataframe with the fragments starts.
    """
    oligos = oligos_correction(oligos_path)
    L_starts = []
    for i in range(len(oligos)):
        oligos_chr = oligos['chr'][i]
        middle = int((oligos['end'][i] - oligos['start'][i] - 1) / 2 + oligos['start'][i] - 1)
        if oligos_chr == 'chr_artificial':
            for k in reversed(range(len(fragments))):
                interval = range(fragments['start'][k], fragments['end'][k])
                fragments_chr = fragments['chr'][k]
                if middle in interval and fragments_chr == oligos_chr:
                    L_starts.append(fragments['start'][k])
                    break
        else:
            for k in range(len(fragments)):
                interval = range(fragments['start'][k], fragments['end'][k] + 1)
                fragments_chr = fragments['chr'][k]

                # if (oligos['start'][i] - 1 in interval and oligos['end'][i] not in interval
                #     or oligos['end'][i] in interval and oligos['start'][i] - 1 not in interval) \
                #         and (middle in interval) \
                #         and (fragments_chr == oligos_chr):
                # print("Warning : Oligo " + str(i) + " overlaps on 2 fragments. \n"
                #                                     "The programm will chose the fragments"
                #                                     " at the middle \n")
                if middle in interval and fragments_chr == oligos_chr:
                    L_starts.append(fragments['start'][k])
                    break
    oligos['start'] = list(L_starts)
    return oligos


def pre_filtering(fragments_path, oligos_path):
    """
    Removes the fragments that does not contains an oligo region
    """
    fragments = fragments_correction(fragments_path)
    oligos = starts_match(fragments, oligos_path)
    oligos.set_index(['chr', 'start'])
    oligos.pop("end")
    fragments.set_index(['chr', 'start'])
    fragments_filtered = fragments.merge(oligos, on=['chr', 'start'])
    fragments_filtered.sort_values(by=['chr', 'start'])
    return fragments_filtered, oligos


def contacts_correction(contacts_path):
    contacts = pd.read_csv(contacts_path, sep='\t', header=None)
    contacts.drop([0], inplace=True)
    contacts.reset_index(drop=True, inplace=True)
    contacts.columns = ['frag_a', 'frag_b', 'contacts']

    return contacts


def first_join(x, fragments_filtered, contacts):
    """

    """
    joined = contacts.join(fragments_filtered, on=x, how='right')
    return joined


def frag2(x):
    if x == 'frag_a':
        y = 'frag_b'
    else:
        y = 'frag_a'
    return y


def second_join(x, oligos, fragments_path, fragments_filtered, contacts):
    fragments = fragments_correction(fragments_path)
    fragments.pop("frag")
    fragments = fragments.merge(oligos, on=['chr', 'start'], how='left')
    contacts = first_join(x, fragments_filtered, contacts)
    # print(contacts.columns)
    y = frag2(x)
    joined = contacts.join(fragments, on=y,
                           lsuffix='_' + x[-1],
                           rsuffix='_' + y[-1], how='left')
    return joined


def concatenation(oligos_path, fragments_path, contacts_path, output_path):
    contacts = contacts_correction(contacts_path)
    fragments_filtered, oligos = pre_filtering(fragments_path, oligos_path)
    fragments_filtered.set_index('frag', inplace=True)
    df1 = second_join('frag_a', oligos, fragments_path, fragments_filtered, contacts)
    # print(df1.columns)
    df2 = second_join('frag_b', oligos, fragments_path, fragments_filtered, contacts)

    df2.reindex(columns=df1.columns)
    contacts_joined = pd.concat([df1, df2])
    contacts_joined.sort_values(by=['frag_a', 'frag_b', 'start_a', 'start_b'], inplace=True)
    contacts_filtered = contacts_joined.convert_dtypes().reset_index(drop=True)
    new = contacts_filtered
    oligos_columns = list(oligos.columns)
    # print(oligos_columns)
    oligos_columns.remove("chr")
    oligos_columns.remove("start")

    for k in oligos.columns:
        name_a = k + '_a'
        name_b = k + '_b'
        # print(new.columns)
        columns = list(new.columns)
        columns.remove(name_a)
        columns.remove(name_b)
        new.rename(columns={name_a: "a", name_b: "b"}, inplace=True)
        # print("columns : ", columns)
        new.set_index(list(columns), inplace=True)
        # print(new)
        # print("colonnes après set_index : ", list(new.columns))
        new = new.stack()
        # print(new)
        new = new.unstack()
        new.convert_dtypes().to_csv(output_path, index=False)
        # print(new)
        # print("colonnes après stack : ", list(new.columns))

    new.convert_dtypes().to_csv(output_path, index=False)


# oligo_path = '/Users/loqmenanani/OneDrive/ENS/L3_ENS/Stage_L3/Projet_cbp/Pycharm/outputs/' \
#              'new_capture_oligos.csv'
# fragments_paths = '/Users/loqmenanani/OneDrive/ENS/L3_ENS/Stage_L3/Projet_cbp/Pycharm/outputs/pre_filtering.txt'
# contacts_paths = 'file:///Users/loqmenanani/OneDrive/ENS/L3_ENS/Stage_L3/' \
#                  'Projet_cbp/Pycharm/inputs/abs_fragments_contacts_weighted.txt'
#
# output_path = '/Users/loqmenanani/OneDrive/ENS/L3_ENS/Stage_L3/Projet_cbp/Pycharm/outputs/fragments_joined_a.txt'


oligo_path = 'Projet/Pycharm/outputs/new_capture_oligos.csv'
fragments_paths = 'Projet/Pycharm/inputs/fragments_list.txt'
contacts_paths = 'Projet/Pycharm/inputs/abs_fragments_contacts_weighted.txt'
outputs_path = 'Projet/Pycharm/outputs/contacts_filtered.csv'
concatenation(oligo_path, fragments_paths, contacts_paths, outputs_path)


contact = pd.read_csv(outputs_path).convert_dtypes()
# print(list(contact.columns))
L = ['name_a', 'type_a', 'sequence_a', 'name_b', 'type_b', 'sequence_b']
contact.rename(columns={"name_a": "a", "name_b": "b"}, inplace=True)


# new = contact.set_index(["frag_a", "frag_b", "contacts", "chr_a", "start_a", "end_a", "size_a",
#                          "gc_content_a", "chr_b", "start_b", "end_b", "size_b", "gc_content_b",
#                          'type_a', 'sequence_a', 'type_b', 'sequence_b'])


# for k in L:
#     print(k)
#     L = ['name_a', 'type_a', 'sequence_a', 'name_b', 'type_b', 'sequence_b']
#     L.remove(k)
#     print(type(new))
#     new = contact.set_index(["frag_a", "frag_b", "contacts", "chr_a", "start_a", "end_a", "size_a",
#                              "gc_content_a", "chr_b", "start_b", "size_b", "gc_content_b"] + L)
#     new = new.stack(dropna=True)

# new.to_csv('/scratch/lanani/Stage_L3_cbp/Projet/Pycharm/outputs/contacts_filtered_indexed.csv')


# a = concatenation(oligo_path, fragments_paths, contacts_paths, outputs_path)
# a.to_csv('/scratch/lanani/Stage_L3_cbp/Projet/Pycharm/outputs/contacts_filtered.csv', sep=',')
# print('lu')
# L_start = f.starts_match(fragments_paths, oligo_path)
# for k in range(len(a)):
#     start_a = a['start_a'][k]
#     start_b = a['start_b'][k]
#     if start_a not in L_start or start_b not in L_start:
#         print('1 sur 2')
#
# print('fin')


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print('Please enter arguments correctly')
        exit(0)

    try:
        opts, args = getopt.getopt(argv, "ho:f:c:O:", ["--help",
                                                       "--oligos",
                                                       "--fragments",
                                                       "--contacts",
                                                       "--output"])
    except getopt.GetoptError:
        print('contacts filter arguments :\n'
              '-o <oligos_input.csv> \n'
              '-f <fragments_input.txt> (generated by hicstuff) \n'
              '-c <contacts_input.txt> (generated by hicstuff) \n'
              '-O <output_contacts_filtered.csv>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('contacts filter arguments :\n'
                  '-o <oligos_input.csv> \n'
                  '-f <fragments_input.txt> (generated by hicstuff) \n'
                  '-c <contacts_input.txt> (generated by hicstuff) \n'
                  '-O <output_contacts_filtered.csv>\n')
            sys.exit()
        elif opt in ("-o", "--oligos"):
            oligos_input = arg
        elif opt in ("-f", "--fragments"):
            fragments_input = arg
        elif opt in ("-c", "--contacts"):
            contacts_input = arg
        elif opt in ("-O", "--output"):
            output_contacts_filtered = arg

    concatenation(oligos_input, fragments_input, contacts_input, output_contacts_filtered)


if __name__ == "__main__":
    main(sys.argv[1:])
