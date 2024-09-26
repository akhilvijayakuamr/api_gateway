# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: post_service.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'post_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12post_service.proto\x12\x0cpost_service\"f\n\x11\x43reatePostRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\r\n\x05title\x18\x02 \x01(\t\x12\x12\n\npost_image\x18\x03 \x01(\x0c\x12\x0f\n\x07\x63ontent\x18\x04 \x01(\t\x12\x0c\n\x04link\x18\x05 \x01(\t\"6\n\x12\x43reatePostResponse\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t\"$\n\x11GetAllPostRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\"\xb0\x01\n\x04Post\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\x0f\n\x07user_id\x18\x02 \x01(\x05\x12\r\n\x05title\x18\x03 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x04 \x01(\t\x12\x0c\n\x04link\x18\x05 \x01(\t\x12\x0c\n\x04\x64\x61te\x18\x06 \x01(\t\x12\x11\n\tpostimage\x18\x07 \x01(\t\x12\x0c\n\x04like\x18\x08 \x01(\x08\x12\x12\n\nlike_count\x18\t \x01(\x05\x12\x15\n\rcomment_count\x18\n \x01(\x05\"7\n\x12GetAllPostResponse\x12!\n\x05posts\x18\x01 \x03(\x0b\x32\x12.post_service.Post\"y\n\x05Reply\x12\x11\n\treplay_id\x18\x01 \x01(\x05\x12\x0f\n\x07user_id\x18\x02 \x01(\x05\x12\x17\n\x0fmention_user_id\x18\x03 \x01(\x05\x12\x14\n\x0cmention_user\x18\x04 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x05 \x01(\t\x12\x0c\n\x04\x64\x61te\x18\x06 \x01(\t\"\x88\x01\n\x07\x43omment\x12\x12\n\ncomment_id\x18\x01 \x01(\x05\x12\x0f\n\x07user_id\x18\x02 \x01(\x05\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\x12\x0c\n\x04\x64\x61te\x18\x04 \x01(\t\x12\x13\n\x0breply_count\x18\x05 \x01(\x05\x12$\n\x07replies\x18\x06 \x03(\x0b\x32\x13.post_service.Reply\"8\n\x14GetUniquePostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\x0f\n\x07user_id\x18\x02 \x01(\x05\"\xea\x01\n\x15GetUniquePostResponse\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\x0f\n\x07user_id\x18\x02 \x01(\x05\x12\r\n\x05title\x18\x03 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x04 \x01(\t\x12\x0c\n\x04link\x18\x05 \x01(\t\x12\x0c\n\x04\x64\x61te\x18\x06 \x01(\t\x12\x11\n\tpostimage\x18\x07 \x01(\t\x12\x0c\n\x04like\x18\x08 \x01(\x08\x12\x12\n\nlike_count\x18\t \x01(\x05\x12\x15\n\rcomment_count\x18\n \x01(\x05\x12\'\n\x08\x63omments\x18\x0b \x03(\x0b\x32\x15.post_service.Comment\"3\n\x0fLikePostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\x0f\n\x07user_id\x18\x02 \x01(\x05\"#\n\x10LikePostResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"G\n\x12\x43ommentPostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\x0f\n\x07user_id\x18\x02 \x01(\x05\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\"&\n\x13\x43ommentPostResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x83\x01\n\x13\x43ommentReplyRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\x17\n\x0fmention_user_id\x18\x02 \x01(\x05\x12\x12\n\ncomment_id\x18\x03 \x01(\x05\x12\x1d\n\x15mention_user_fullname\x18\x04 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x05 \x01(\t\"\'\n\x14\x43ommentReplyResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\")\n\x16UniqueUserPostsRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\"<\n\x17UniqueUserPostsResponse\x12!\n\x05posts\x18\x01 \x03(\x0b\x32\x12.post_service.Post2\xdf\x04\n\x0bPostService\x12O\n\nCreatePost\x12\x1f.post_service.CreatePostRequest\x1a .post_service.CreatePostResponse\x12O\n\nGetAllPost\x12\x1f.post_service.GetAllPostRequest\x1a .post_service.GetAllPostResponse\x12X\n\rGetUniquePost\x12\".post_service.GetUniquePostRequest\x1a#.post_service.GetUniquePostResponse\x12I\n\x08LikePost\x12\x1d.post_service.LikePostRequest\x1a\x1e.post_service.LikePostResponse\x12R\n\x0b\x43ommentPost\x12 .post_service.CommentPostRequest\x1a!.post_service.CommentPostResponse\x12U\n\x0c\x43ommentReply\x12!.post_service.CommentReplyRequest\x1a\".post_service.CommentReplyResponse\x12^\n\x0fUniqueUserPosts\x12$.post_service.UniqueUserPostsRequest\x1a%.post_service.UniqueUserPostsResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'post_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CREATEPOSTREQUEST']._serialized_start=36
  _globals['_CREATEPOSTREQUEST']._serialized_end=138
  _globals['_CREATEPOSTRESPONSE']._serialized_start=140
  _globals['_CREATEPOSTRESPONSE']._serialized_end=194
  _globals['_GETALLPOSTREQUEST']._serialized_start=196
  _globals['_GETALLPOSTREQUEST']._serialized_end=232
  _globals['_POST']._serialized_start=235
  _globals['_POST']._serialized_end=411
  _globals['_GETALLPOSTRESPONSE']._serialized_start=413
  _globals['_GETALLPOSTRESPONSE']._serialized_end=468
  _globals['_REPLY']._serialized_start=470
  _globals['_REPLY']._serialized_end=591
  _globals['_COMMENT']._serialized_start=594
  _globals['_COMMENT']._serialized_end=730
  _globals['_GETUNIQUEPOSTREQUEST']._serialized_start=732
  _globals['_GETUNIQUEPOSTREQUEST']._serialized_end=788
  _globals['_GETUNIQUEPOSTRESPONSE']._serialized_start=791
  _globals['_GETUNIQUEPOSTRESPONSE']._serialized_end=1025
  _globals['_LIKEPOSTREQUEST']._serialized_start=1027
  _globals['_LIKEPOSTREQUEST']._serialized_end=1078
  _globals['_LIKEPOSTRESPONSE']._serialized_start=1080
  _globals['_LIKEPOSTRESPONSE']._serialized_end=1115
  _globals['_COMMENTPOSTREQUEST']._serialized_start=1117
  _globals['_COMMENTPOSTREQUEST']._serialized_end=1188
  _globals['_COMMENTPOSTRESPONSE']._serialized_start=1190
  _globals['_COMMENTPOSTRESPONSE']._serialized_end=1228
  _globals['_COMMENTREPLYREQUEST']._serialized_start=1231
  _globals['_COMMENTREPLYREQUEST']._serialized_end=1362
  _globals['_COMMENTREPLYRESPONSE']._serialized_start=1364
  _globals['_COMMENTREPLYRESPONSE']._serialized_end=1403
  _globals['_UNIQUEUSERPOSTSREQUEST']._serialized_start=1405
  _globals['_UNIQUEUSERPOSTSREQUEST']._serialized_end=1446
  _globals['_UNIQUEUSERPOSTSRESPONSE']._serialized_start=1448
  _globals['_UNIQUEUSERPOSTSRESPONSE']._serialized_end=1508
  _globals['_POSTSERVICE']._serialized_start=1511
  _globals['_POSTSERVICE']._serialized_end=2118
# @@protoc_insertion_point(module_scope)
