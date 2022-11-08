from pyscf.data.elements import ELEMENTS

from classiq.interface.chemistry.ground_state_problem import MoleculeProblem

from classiq.applications.chemistry.pyscf_hamiltonian import _to_pyscf_molecule
from classiq.exceptions import ClassiqRemoveOrbitalsError


def get_num_orbitals(molecule_problem: MoleculeProblem) -> int:
    molecule = _to_pyscf_molecule(molecule_problem)
    num_orbitals = 2 * int(molecule.nao)

    if molecule_problem.freeze_core:
        num_orbitals -= 2 * _count_core_orbitals(molecule_problem)

    if molecule_problem.remove_orbitals:
        if not all(
            orbital < num_orbitals // 2 for orbital in molecule_problem.remove_orbitals
        ):
            raise ClassiqRemoveOrbitalsError("removed orbitals are out of bound")

        num_orbitals -= 2 * len(molecule_problem.remove_orbitals)

    return num_orbitals


def _count_core_orbitals(molecule_problem: MoleculeProblem) -> int:
    return sum(
        _get_num_core_electrons(_get_atomic_number(atom))
        for atom, _ in molecule_problem.molecule.atoms
    )


def _get_atomic_number(atom: str) -> int:
    return ELEMENTS.index(atom.lower().capitalize())


def _get_num_core_electrons(atomic_number: int) -> int:
    count = 0
    if atomic_number > 2:
        count += 1
    if atomic_number > 10:
        count += 4
    if atomic_number > 18:
        count += 4
    if atomic_number > 36:
        count += 9
    if atomic_number > 54:
        count += 9
    if atomic_number > 86:
        count += 16

    return count
