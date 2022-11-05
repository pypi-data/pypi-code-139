# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: anki/scheduler.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from anki import generic_pb2 as anki_dot_generic__pb2
from anki import cards_pb2 as anki_dot_cards__pb2
from anki import decks_pb2 as anki_dot_decks__pb2
from anki import collection_pb2 as anki_dot_collection__pb2
from anki import config_pb2 as anki_dot_config__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14\x61nki/scheduler.proto\x12\x0e\x61nki.scheduler\x1a\x12\x61nki/generic.proto\x1a\x10\x61nki/cards.proto\x1a\x10\x61nki/decks.proto\x1a\x15\x61nki/collection.proto\x1a\x11\x61nki/config.proto\"\xae\x08\n\x0fSchedulingState\x12\x38\n\x06normal\x18\x01 \x01(\x0b\x32&.anki.scheduler.SchedulingState.NormalH\x00\x12<\n\x08\x66iltered\x18\x02 \x01(\x0b\x32(.anki.scheduler.SchedulingState.FilteredH\x00\x12\x18\n\x0b\x63ustom_data\x18\x03 \x01(\tH\x01\x88\x01\x01\x1a\x17\n\x03New\x12\x10\n\x08position\x18\x01 \x01(\r\x1a;\n\x08Learning\x12\x17\n\x0fremaining_steps\x18\x01 \x01(\r\x12\x16\n\x0escheduled_secs\x18\x02 \x01(\r\x1al\n\x06Review\x12\x16\n\x0escheduled_days\x18\x01 \x01(\r\x12\x14\n\x0c\x65lapsed_days\x18\x02 \x01(\r\x12\x13\n\x0b\x65\x61se_factor\x18\x03 \x01(\x02\x12\x0e\n\x06lapses\x18\x04 \x01(\r\x12\x0f\n\x07leeched\x18\x05 \x01(\x08\x1a\x80\x01\n\nRelearning\x12\x36\n\x06review\x18\x01 \x01(\x0b\x32&.anki.scheduler.SchedulingState.Review\x12:\n\x08learning\x18\x02 \x01(\x0b\x32(.anki.scheduler.SchedulingState.Learning\x1a\xff\x01\n\x06Normal\x12\x32\n\x03new\x18\x01 \x01(\x0b\x32#.anki.scheduler.SchedulingState.NewH\x00\x12<\n\x08learning\x18\x02 \x01(\x0b\x32(.anki.scheduler.SchedulingState.LearningH\x00\x12\x38\n\x06review\x18\x03 \x01(\x0b\x32&.anki.scheduler.SchedulingState.ReviewH\x00\x12@\n\nrelearning\x18\x04 \x01(\x0b\x32*.anki.scheduler.SchedulingState.RelearningH\x00\x42\x07\n\x05value\x1a\x33\n\x07Preview\x12\x16\n\x0escheduled_secs\x18\x01 \x01(\r\x12\x10\n\x08\x66inished\x18\x02 \x01(\x08\x1aT\n\x12ReschedulingFilter\x12>\n\x0eoriginal_state\x18\x01 \x01(\x0b\x32&.anki.scheduler.SchedulingState.Normal\x1a\x9b\x01\n\x08\x46iltered\x12:\n\x07preview\x18\x01 \x01(\x0b\x32\'.anki.scheduler.SchedulingState.PreviewH\x00\x12J\n\x0crescheduling\x18\x02 \x01(\x0b\x32\x32.anki.scheduler.SchedulingState.ReschedulingFilterH\x00\x42\x07\n\x05valueB\x07\n\x05valueB\x0e\n\x0c_custom_data\"\xc4\x02\n\x0bQueuedCards\x12\x35\n\x05\x63\x61rds\x18\x01 \x03(\x0b\x32&.anki.scheduler.QueuedCards.QueuedCard\x12\x11\n\tnew_count\x18\x02 \x01(\r\x12\x16\n\x0elearning_count\x18\x03 \x01(\r\x12\x14\n\x0creview_count\x18\x04 \x01(\r\x1a\x90\x01\n\nQueuedCard\x12\x1e\n\x04\x63\x61rd\x18\x01 \x01(\x0b\x32\x10.anki.cards.Card\x12\x30\n\x05queue\x18\x02 \x01(\x0e\x32!.anki.scheduler.QueuedCards.Queue\x12\x30\n\x06states\x18\x03 \x01(\x0b\x32 .anki.scheduler.SchedulingStates\"*\n\x05Queue\x12\x07\n\x03NEW\x10\x00\x12\x0c\n\x08LEARNING\x10\x01\x12\n\n\x06REVIEW\x10\x02\"L\n\x15GetQueuedCardsRequest\x12\x13\n\x0b\x66\x65tch_limit\x18\x01 \x01(\r\x12\x1e\n\x16intraday_learning_only\x18\x02 \x01(\x08\"E\n\x18SchedTimingTodayResponse\x12\x14\n\x0c\x64\x61ys_elapsed\x18\x01 \x01(\r\x12\x13\n\x0bnext_day_at\x18\x02 \x01(\x03\"<\n\x1aStudiedTodayMessageRequest\x12\r\n\x05\x63\x61rds\x18\x01 \x01(\r\x12\x0f\n\x07seconds\x18\x02 \x01(\x01\"i\n\x12UpdateStatsRequest\x12\x0f\n\x07\x64\x65\x63k_id\x18\x01 \x01(\x03\x12\x11\n\tnew_delta\x18\x02 \x01(\x05\x12\x14\n\x0creview_delta\x18\x04 \x01(\x05\x12\x19\n\x11millisecond_delta\x18\x05 \x01(\x05\"O\n\x13\x45xtendLimitsRequest\x12\x0f\n\x07\x64\x65\x63k_id\x18\x01 \x01(\x03\x12\x11\n\tnew_delta\x18\x02 \x01(\x05\x12\x14\n\x0creview_delta\x18\x03 \x01(\x05\"9\n\x1a\x43ountsForDeckTodayResponse\x12\x0b\n\x03new\x18\x01 \x01(\x05\x12\x0e\n\x06review\x18\x02 \x01(\x05\"\x8b\x02\n\x14\x43ongratsInfoResponse\x12\x17\n\x0flearn_remaining\x18\x01 \x01(\r\x12\x1d\n\x15secs_until_next_learn\x18\x02 \x01(\r\x12\x18\n\x10review_remaining\x18\x03 \x01(\x08\x12\x15\n\rnew_remaining\x18\x04 \x01(\x08\x12\x19\n\x11have_sched_buried\x18\x05 \x01(\x08\x12\x18\n\x10have_user_buried\x18\x06 \x01(\x08\x12\x18\n\x10is_filtered_deck\x18\x07 \x01(\x08\x12!\n\x19\x62ridge_commands_supported\x18\x08 \x01(\x08\x12\x18\n\x10\x64\x65\x63k_description\x18\t \x01(\t\"\x8a\x01\n\x11UnburyDeckRequest\x12\x0f\n\x07\x64\x65\x63k_id\x18\x01 \x01(\x03\x12\x34\n\x04mode\x18\x02 \x01(\x0e\x32&.anki.scheduler.UnburyDeckRequest.Mode\".\n\x04Mode\x12\x07\n\x03\x41LL\x10\x00\x12\x0e\n\nSCHED_ONLY\x10\x01\x12\r\n\tUSER_ONLY\x10\x02\"\xb1\x01\n\x19\x42uryOrSuspendCardsRequest\x12\x10\n\x08\x63\x61rd_ids\x18\x01 \x03(\x03\x12\x10\n\x08note_ids\x18\x02 \x03(\x03\x12<\n\x04mode\x18\x03 \x01(\x0e\x32..anki.scheduler.BuryOrSuspendCardsRequest.Mode\"2\n\x04Mode\x12\x0b\n\x07SUSPEND\x10\x00\x12\x0e\n\nBURY_SCHED\x10\x01\x12\r\n\tBURY_USER\x10\x02\"\xe5\x01\n\x19ScheduleCardsAsNewRequest\x12\x10\n\x08\x63\x61rd_ids\x18\x01 \x03(\x03\x12\x0b\n\x03log\x18\x02 \x01(\x08\x12\x18\n\x10restore_position\x18\x03 \x01(\x08\x12\x14\n\x0creset_counts\x18\x04 \x01(\x08\x12G\n\x07\x63ontext\x18\x05 \x01(\x0e\x32\x31.anki.scheduler.ScheduleCardsAsNewRequest.ContextH\x00\x88\x01\x01\"$\n\x07\x43ontext\x12\x0b\n\x07\x42ROWSER\x10\x00\x12\x0c\n\x08REVIEWER\x10\x01\x42\n\n\x08_context\"g\n!ScheduleCardsAsNewDefaultsRequest\x12\x42\n\x07\x63ontext\x18\x01 \x01(\x0e\x32\x31.anki.scheduler.ScheduleCardsAsNewRequest.Context\"T\n\"ScheduleCardsAsNewDefaultsResponse\x12\x18\n\x10restore_position\x18\x01 \x01(\x08\x12\x14\n\x0creset_counts\x18\x02 \x01(\x08\"m\n\x11SetDueDateRequest\x12\x10\n\x08\x63\x61rd_ids\x18\x01 \x03(\x03\x12\x0c\n\x04\x64\x61ys\x18\x02 \x01(\t\x12\x38\n\nconfig_key\x18\x03 \x01(\x0b\x32$.anki.config.OptionalStringConfigKey\"y\n\x10SortCardsRequest\x12\x10\n\x08\x63\x61rd_ids\x18\x01 \x03(\x03\x12\x15\n\rstarting_from\x18\x02 \x01(\r\x12\x11\n\tstep_size\x18\x03 \x01(\r\x12\x11\n\trandomize\x18\x04 \x01(\x08\x12\x16\n\x0eshift_existing\x18\x05 \x01(\x08\"5\n\x0fSortDeckRequest\x12\x0f\n\x07\x64\x65\x63k_id\x18\x01 \x01(\x03\x12\x11\n\trandomize\x18\x02 \x01(\x08\"\x81\x02\n\x10SchedulingStates\x12\x30\n\x07\x63urrent\x18\x01 \x01(\x0b\x32\x1f.anki.scheduler.SchedulingState\x12.\n\x05\x61gain\x18\x02 \x01(\x0b\x32\x1f.anki.scheduler.SchedulingState\x12-\n\x04hard\x18\x03 \x01(\x0b\x32\x1f.anki.scheduler.SchedulingState\x12-\n\x04good\x18\x04 \x01(\x0b\x32\x1f.anki.scheduler.SchedulingState\x12-\n\x04\x65\x61sy\x18\x05 \x01(\x0b\x32\x1f.anki.scheduler.SchedulingState\"\xa7\x02\n\nCardAnswer\x12\x0f\n\x07\x63\x61rd_id\x18\x01 \x01(\x03\x12\x36\n\rcurrent_state\x18\x02 \x01(\x0b\x32\x1f.anki.scheduler.SchedulingState\x12\x32\n\tnew_state\x18\x03 \x01(\x0b\x32\x1f.anki.scheduler.SchedulingState\x12\x31\n\x06rating\x18\x04 \x01(\x0e\x32!.anki.scheduler.CardAnswer.Rating\x12\x1a\n\x12\x61nswered_at_millis\x18\x05 \x01(\x03\x12\x1a\n\x12milliseconds_taken\x18\x06 \x01(\r\"1\n\x06Rating\x12\t\n\x05\x41GAIN\x10\x00\x12\x08\n\x04HARD\x10\x01\x12\x08\n\x04GOOD\x10\x02\x12\x08\n\x04\x45\x41SY\x10\x03\"\xd6\x03\n\x12\x43ustomStudyRequest\x12\x0f\n\x07\x64\x65\x63k_id\x18\x01 \x01(\x03\x12\x19\n\x0fnew_limit_delta\x18\x02 \x01(\x05H\x00\x12\x1c\n\x12review_limit_delta\x18\x03 \x01(\x05H\x00\x12\x15\n\x0b\x66orgot_days\x18\x04 \x01(\rH\x00\x12\x1b\n\x11review_ahead_days\x18\x05 \x01(\rH\x00\x12\x16\n\x0cpreview_days\x18\x06 \x01(\rH\x00\x12\x37\n\x04\x63ram\x18\x07 \x01(\x0b\x32\'.anki.scheduler.CustomStudyRequest.CramH\x00\x1a\xe7\x01\n\x04\x43ram\x12>\n\x04kind\x18\x01 \x01(\x0e\x32\x30.anki.scheduler.CustomStudyRequest.Cram.CramKind\x12\x12\n\ncard_limit\x18\x02 \x01(\r\x12\x17\n\x0ftags_to_include\x18\x03 \x03(\t\x12\x17\n\x0ftags_to_exclude\x18\x04 \x03(\t\"Y\n\x08\x43ramKind\x12\x11\n\rCRAM_KIND_DUE\x10\x00\x12\x11\n\rCRAM_KIND_NEW\x10\x01\x12\x14\n\x10\x43RAM_KIND_REVIEW\x10\x02\x12\x11\n\rCRAM_KIND_ALL\x10\x03\x42\x07\n\x05value\"-\n\x1a\x43ustomStudyDefaultsRequest\x12\x0f\n\x07\x64\x65\x63k_id\x18\x01 \x01(\x03\"\xb8\x02\n\x1b\x43ustomStudyDefaultsResponse\x12=\n\x04tags\x18\x01 \x03(\x0b\x32/.anki.scheduler.CustomStudyDefaultsResponse.Tag\x12\x12\n\nextend_new\x18\x02 \x01(\r\x12\x15\n\rextend_review\x18\x03 \x01(\r\x12\x15\n\ravailable_new\x18\x04 \x01(\r\x12\x18\n\x10\x61vailable_review\x18\x05 \x01(\r\x12!\n\x19\x61vailable_new_in_children\x18\x06 \x01(\r\x12$\n\x1c\x61vailable_review_in_children\x18\x07 \x01(\r\x1a\x35\n\x03Tag\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07include\x18\x02 \x01(\x08\x12\x0f\n\x07\x65xclude\x18\x03 \x01(\x08\";\n\x1aRepositionDefaultsResponse\x12\x0e\n\x06random\x18\x01 \x01(\x08\x12\r\n\x05shift\x18\x02 \x01(\x08\x32\xf1\x10\n\x10SchedulerService\x12T\n\x0eGetQueuedCards\x12%.anki.scheduler.GetQueuedCardsRequest\x1a\x1b.anki.scheduler.QueuedCards\x12\x44\n\nAnswerCard\x12\x1a.anki.scheduler.CardAnswer\x1a\x1a.anki.collection.OpChanges\x12Q\n\x10SchedTimingToday\x12\x13.anki.generic.Empty\x1a(.anki.scheduler.SchedTimingTodayResponse\x12\x39\n\x0cStudiedToday\x12\x13.anki.generic.Empty\x1a\x14.anki.generic.String\x12W\n\x13StudiedTodayMessage\x12*.anki.scheduler.StudiedTodayMessageRequest\x1a\x14.anki.generic.String\x12\x46\n\x0bUpdateStats\x12\".anki.scheduler.UpdateStatsRequest\x1a\x13.anki.generic.Empty\x12H\n\x0c\x45xtendLimits\x12#.anki.scheduler.ExtendLimitsRequest\x1a\x13.anki.generic.Empty\x12T\n\x12\x43ountsForDeckToday\x12\x12.anki.decks.DeckId\x1a*.anki.scheduler.CountsForDeckTodayResponse\x12I\n\x0c\x43ongratsInfo\x12\x13.anki.generic.Empty\x1a$.anki.scheduler.CongratsInfoResponse\x12Q\n\x1eRestoreBuriedAndSuspendedCards\x12\x13.anki.cards.CardIds\x1a\x1a.anki.collection.OpChanges\x12K\n\nUnburyDeck\x12!.anki.scheduler.UnburyDeckRequest\x1a\x1a.anki.collection.OpChanges\x12\x64\n\x12\x42uryOrSuspendCards\x12).anki.scheduler.BuryOrSuspendCardsRequest\x1a#.anki.collection.OpChangesWithCount\x12\x43\n\x11\x45mptyFilteredDeck\x12\x12.anki.decks.DeckId\x1a\x1a.anki.collection.OpChanges\x12N\n\x13RebuildFilteredDeck\x12\x12.anki.decks.DeckId\x1a#.anki.collection.OpChangesWithCount\x12[\n\x12ScheduleCardsAsNew\x12).anki.scheduler.ScheduleCardsAsNewRequest\x1a\x1a.anki.collection.OpChanges\x12\x83\x01\n\x1aScheduleCardsAsNewDefaults\x12\x31.anki.scheduler.ScheduleCardsAsNewDefaultsRequest\x1a\x32.anki.scheduler.ScheduleCardsAsNewDefaultsResponse\x12K\n\nSetDueDate\x12!.anki.scheduler.SetDueDateRequest\x1a\x1a.anki.collection.OpChanges\x12R\n\tSortCards\x12 .anki.scheduler.SortCardsRequest\x1a#.anki.collection.OpChangesWithCount\x12P\n\x08SortDeck\x12\x1f.anki.scheduler.SortDeckRequest\x1a#.anki.collection.OpChangesWithCount\x12K\n\x13GetSchedulingStates\x12\x12.anki.cards.CardId\x1a .anki.scheduler.SchedulingStates\x12P\n\x12\x44\x65scribeNextStates\x12 .anki.scheduler.SchedulingStates\x1a\x18.anki.generic.StringList\x12\x43\n\x0cStateIsLeech\x12\x1f.anki.scheduler.SchedulingState\x1a\x12.anki.generic.Bool\x12<\n\x10UpgradeScheduler\x12\x13.anki.generic.Empty\x1a\x13.anki.generic.Empty\x12M\n\x0b\x43ustomStudy\x12\".anki.scheduler.CustomStudyRequest\x1a\x1a.anki.collection.OpChanges\x12n\n\x13\x43ustomStudyDefaults\x12*.anki.scheduler.CustomStudyDefaultsRequest\x1a+.anki.scheduler.CustomStudyDefaultsResponse\x12U\n\x12RepositionDefaults\x12\x13.anki.generic.Empty\x1a*.anki.scheduler.RepositionDefaultsResponseB\x02P\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'anki.scheduler_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'P\001'
  _SCHEDULINGSTATE._serialized_start=139
  _SCHEDULINGSTATE._serialized_end=1209
  _SCHEDULINGSTATE_NEW._serialized_start=304
  _SCHEDULINGSTATE_NEW._serialized_end=327
  _SCHEDULINGSTATE_LEARNING._serialized_start=329
  _SCHEDULINGSTATE_LEARNING._serialized_end=388
  _SCHEDULINGSTATE_REVIEW._serialized_start=390
  _SCHEDULINGSTATE_REVIEW._serialized_end=498
  _SCHEDULINGSTATE_RELEARNING._serialized_start=501
  _SCHEDULINGSTATE_RELEARNING._serialized_end=629
  _SCHEDULINGSTATE_NORMAL._serialized_start=632
  _SCHEDULINGSTATE_NORMAL._serialized_end=887
  _SCHEDULINGSTATE_PREVIEW._serialized_start=889
  _SCHEDULINGSTATE_PREVIEW._serialized_end=940
  _SCHEDULINGSTATE_RESCHEDULINGFILTER._serialized_start=942
  _SCHEDULINGSTATE_RESCHEDULINGFILTER._serialized_end=1026
  _SCHEDULINGSTATE_FILTERED._serialized_start=1029
  _SCHEDULINGSTATE_FILTERED._serialized_end=1184
  _QUEUEDCARDS._serialized_start=1212
  _QUEUEDCARDS._serialized_end=1536
  _QUEUEDCARDS_QUEUEDCARD._serialized_start=1348
  _QUEUEDCARDS_QUEUEDCARD._serialized_end=1492
  _QUEUEDCARDS_QUEUE._serialized_start=1494
  _QUEUEDCARDS_QUEUE._serialized_end=1536
  _GETQUEUEDCARDSREQUEST._serialized_start=1538
  _GETQUEUEDCARDSREQUEST._serialized_end=1614
  _SCHEDTIMINGTODAYRESPONSE._serialized_start=1616
  _SCHEDTIMINGTODAYRESPONSE._serialized_end=1685
  _STUDIEDTODAYMESSAGEREQUEST._serialized_start=1687
  _STUDIEDTODAYMESSAGEREQUEST._serialized_end=1747
  _UPDATESTATSREQUEST._serialized_start=1749
  _UPDATESTATSREQUEST._serialized_end=1854
  _EXTENDLIMITSREQUEST._serialized_start=1856
  _EXTENDLIMITSREQUEST._serialized_end=1935
  _COUNTSFORDECKTODAYRESPONSE._serialized_start=1937
  _COUNTSFORDECKTODAYRESPONSE._serialized_end=1994
  _CONGRATSINFORESPONSE._serialized_start=1997
  _CONGRATSINFORESPONSE._serialized_end=2264
  _UNBURYDECKREQUEST._serialized_start=2267
  _UNBURYDECKREQUEST._serialized_end=2405
  _UNBURYDECKREQUEST_MODE._serialized_start=2359
  _UNBURYDECKREQUEST_MODE._serialized_end=2405
  _BURYORSUSPENDCARDSREQUEST._serialized_start=2408
  _BURYORSUSPENDCARDSREQUEST._serialized_end=2585
  _BURYORSUSPENDCARDSREQUEST_MODE._serialized_start=2535
  _BURYORSUSPENDCARDSREQUEST_MODE._serialized_end=2585
  _SCHEDULECARDSASNEWREQUEST._serialized_start=2588
  _SCHEDULECARDSASNEWREQUEST._serialized_end=2817
  _SCHEDULECARDSASNEWREQUEST_CONTEXT._serialized_start=2769
  _SCHEDULECARDSASNEWREQUEST_CONTEXT._serialized_end=2805
  _SCHEDULECARDSASNEWDEFAULTSREQUEST._serialized_start=2819
  _SCHEDULECARDSASNEWDEFAULTSREQUEST._serialized_end=2922
  _SCHEDULECARDSASNEWDEFAULTSRESPONSE._serialized_start=2924
  _SCHEDULECARDSASNEWDEFAULTSRESPONSE._serialized_end=3008
  _SETDUEDATEREQUEST._serialized_start=3010
  _SETDUEDATEREQUEST._serialized_end=3119
  _SORTCARDSREQUEST._serialized_start=3121
  _SORTCARDSREQUEST._serialized_end=3242
  _SORTDECKREQUEST._serialized_start=3244
  _SORTDECKREQUEST._serialized_end=3297
  _SCHEDULINGSTATES._serialized_start=3300
  _SCHEDULINGSTATES._serialized_end=3557
  _CARDANSWER._serialized_start=3560
  _CARDANSWER._serialized_end=3855
  _CARDANSWER_RATING._serialized_start=3806
  _CARDANSWER_RATING._serialized_end=3855
  _CUSTOMSTUDYREQUEST._serialized_start=3858
  _CUSTOMSTUDYREQUEST._serialized_end=4328
  _CUSTOMSTUDYREQUEST_CRAM._serialized_start=4088
  _CUSTOMSTUDYREQUEST_CRAM._serialized_end=4319
  _CUSTOMSTUDYREQUEST_CRAM_CRAMKIND._serialized_start=4230
  _CUSTOMSTUDYREQUEST_CRAM_CRAMKIND._serialized_end=4319
  _CUSTOMSTUDYDEFAULTSREQUEST._serialized_start=4330
  _CUSTOMSTUDYDEFAULTSREQUEST._serialized_end=4375
  _CUSTOMSTUDYDEFAULTSRESPONSE._serialized_start=4378
  _CUSTOMSTUDYDEFAULTSRESPONSE._serialized_end=4690
  _CUSTOMSTUDYDEFAULTSRESPONSE_TAG._serialized_start=4637
  _CUSTOMSTUDYDEFAULTSRESPONSE_TAG._serialized_end=4690
  _REPOSITIONDEFAULTSRESPONSE._serialized_start=4692
  _REPOSITIONDEFAULTSRESPONSE._serialized_end=4751
  _SCHEDULERSERVICE._serialized_start=4754
  _SCHEDULERSERVICE._serialized_end=6915
# @@protoc_insertion_point(module_scope)
