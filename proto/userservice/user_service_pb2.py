# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: user_service.proto
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
    'user_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12user_service.proto\x12\x0cuser_service\"Y\n\x11\x43reateUserRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\x12\x10\n\x08password\x18\x04 \x01(\t\"Y\n\x04User\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\x12\r\n\x05\x65mail\x18\x04 \x01(\t\x12\x11\n\tis_active\x18\x05 \x01(\x08\"4\n\x12\x43reateUserResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\r\n\x05\x65rror\x18\x02 \x01(\t\".\n\x10VerifyOtpRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x0b\n\x03otp\x18\x02 \x01(\t\"3\n\x11VerifyOtpResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\r\n\x05\x65rror\x18\x02 \x01(\t\"!\n\x10ResendOtpRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\"3\n\x11ResendOtpResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\r\n\x05\x65rror\x18\x02 \x01(\t\"E\n\x10LoginUserRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x10\n\x08provider\x18\x03 \x01(\t\"Y\n\rLoginResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x0b\n\x03jwt\x18\x03 \x01(\t\x12\x0f\n\x07message\x18\x04 \x01(\t\x12\x0f\n\x07profile\x18\x05 \x01(\t\"4\n\x11LoginAdminRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"2\n\x12LoginAdminResponse\x12\x0b\n\x03jwt\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\"\x11\n\x0fUserListRequest\"5\n\x10UserListResponse\x12!\n\x05users\x18\x01 \x03(\x0b\x32\x12.user_service.User\"\x1c\n\x0b\x41uthRequest\x12\r\n\x05token\x18\x01 \x01(\t\"H\n\x0c\x41uthResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05\x61\x64min\x18\x02 \x01(\x08\x12\x0c\n\x04user\x18\x03 \x01(\x08\x12\x0f\n\x07message\x18\x04 \x01(\t\"!\n\x13\x42lockUnBlockRequest\x12\n\n\x02id\x18\x01 \x01(\t\"\'\n\x14\x42lockUnBlockResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\" \n\x12ProfileDataRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"\x9c\x01\n\x13ProfileDataResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\x12\x10\n\x08location\x18\x04 \x01(\t\x12\x0b\n\x03\x62io\x18\x05 \x01(\t\x12\x0b\n\x03\x64ob\x18\x06 \x01(\t\x12\x14\n\x0cprofileimage\x18\x07 \x01(\t\x12\x12\n\ncoverimage\x18\x08 \x01(\t\"\x9d\x01\n\x14ProfileUpdateRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\x12\x10\n\x08location\x18\x04 \x01(\t\x12\x0b\n\x03\x62io\x18\x05 \x01(\t\x12\x0b\n\x03\x64ob\x18\x06 \x01(\t\x12\x14\n\x0cprofileimage\x18\x08 \x01(\x0c\x12\x12\n\ncoverimage\x18\t \x01(\x0c\"7\n\x15ProfileUpdateResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\r\n\x05\x65rror\x18\x02 \x01(\t\"5\n\x11GoogleUserRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x11\n\tfull_name\x18\x02 \x01(\t\"M\n\x12GoogleUserResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x0b\n\x03jwt\x18\x03 \x01(\t\x12\x0f\n\x07message\x18\x04 \x01(\t\"$\n\x13\x46orgoteEmailRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\"\'\n\x14\x46orgoteEmailResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"8\n\x15\x43hangePasswordRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\")\n\x16\x43hangePasswordResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"%\n\x12PostProfileRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\",\n\x13PostProfileResponse\x12\x15\n\rprofile_image\x18\x01 \x01(\t\"(\n\x15PostUniqueDataRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\"a\n\x16PostUniqueDataResponse\x12\x11\n\tfull_name\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x15\n\rprofile_image\x18\x03 \x01(\t\x12\x0b\n\x03\x62io\x18\x04 \x01(\t\"+\n\x18\x43ommentUniqueDataRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\"D\n\x19\x43ommentUniqueDataResponse\x12\x11\n\tfull_name\x18\x01 \x01(\t\x12\x14\n\x0cuser_profile\x18\x02 \x01(\t2\xcc\n\n\x0bUserService\x12O\n\nCreateUser\x12\x1f.user_service.CreateUserRequest\x1a .user_service.CreateUserResponse\x12L\n\tVerifyOtp\x12\x1e.user_service.VerifyOtpRequest\x1a\x1f.user_service.VerifyOtpResponse\x12H\n\tLoginUser\x12\x1e.user_service.LoginUserRequest\x1a\x1b.user_service.LoginResponse\x12O\n\nGoogleUser\x12\x1f.user_service.GoogleUserRequest\x1a .user_service.GoogleUserResponse\x12O\n\nLoginAdmin\x12\x1f.user_service.LoginAdminRequest\x1a .user_service.LoginAdminResponse\x12L\n\tResendOtp\x12\x1e.user_service.ResendOtpRequest\x1a\x1f.user_service.ResendOtpResponse\x12I\n\x08UserList\x12\x1d.user_service.UserListRequest\x1a\x1e.user_service.UserListResponse\x12\x46\n\rAutherization\x12\x19.user_service.AuthRequest\x1a\x1a.user_service.AuthResponse\x12Y\n\x10\x42lockUnblockUser\x12!.user_service.BlockUnBlockRequest\x1a\".user_service.BlockUnBlockResponse\x12R\n\x0bProfileData\x12 .user_service.ProfileDataRequest\x1a!.user_service.ProfileDataResponse\x12X\n\rProfileUpdate\x12\".user_service.ProfileUpdateRequest\x1a#.user_service.ProfileUpdateResponse\x12T\n\x0b\x46orgotEmail\x12!.user_service.ForgoteEmailRequest\x1a\".user_service.ForgoteEmailResponse\x12[\n\x0e\x43hangePassword\x12#.user_service.ChangePasswordRequest\x1a$.user_service.ChangePasswordResponse\x12R\n\x0bPostProfile\x12 .user_service.PostProfileRequest\x1a!.user_service.PostProfileResponse\x12[\n\x0ePostUniqueData\x12#.user_service.PostUniqueDataRequest\x1a$.user_service.PostUniqueDataResponse\x12\x64\n\x11\x43ommentUniqueData\x12&.user_service.CommentUniqueDataRequest\x1a\'.user_service.CommentUniqueDataResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'user_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CREATEUSERREQUEST']._serialized_start=36
  _globals['_CREATEUSERREQUEST']._serialized_end=125
  _globals['_USER']._serialized_start=127
  _globals['_USER']._serialized_end=216
  _globals['_CREATEUSERRESPONSE']._serialized_start=218
  _globals['_CREATEUSERRESPONSE']._serialized_end=270
  _globals['_VERIFYOTPREQUEST']._serialized_start=272
  _globals['_VERIFYOTPREQUEST']._serialized_end=318
  _globals['_VERIFYOTPRESPONSE']._serialized_start=320
  _globals['_VERIFYOTPRESPONSE']._serialized_end=371
  _globals['_RESENDOTPREQUEST']._serialized_start=373
  _globals['_RESENDOTPREQUEST']._serialized_end=406
  _globals['_RESENDOTPRESPONSE']._serialized_start=408
  _globals['_RESENDOTPRESPONSE']._serialized_end=459
  _globals['_LOGINUSERREQUEST']._serialized_start=461
  _globals['_LOGINUSERREQUEST']._serialized_end=530
  _globals['_LOGINRESPONSE']._serialized_start=532
  _globals['_LOGINRESPONSE']._serialized_end=621
  _globals['_LOGINADMINREQUEST']._serialized_start=623
  _globals['_LOGINADMINREQUEST']._serialized_end=675
  _globals['_LOGINADMINRESPONSE']._serialized_start=677
  _globals['_LOGINADMINRESPONSE']._serialized_end=727
  _globals['_USERLISTREQUEST']._serialized_start=729
  _globals['_USERLISTREQUEST']._serialized_end=746
  _globals['_USERLISTRESPONSE']._serialized_start=748
  _globals['_USERLISTRESPONSE']._serialized_end=801
  _globals['_AUTHREQUEST']._serialized_start=803
  _globals['_AUTHREQUEST']._serialized_end=831
  _globals['_AUTHRESPONSE']._serialized_start=833
  _globals['_AUTHRESPONSE']._serialized_end=905
  _globals['_BLOCKUNBLOCKREQUEST']._serialized_start=907
  _globals['_BLOCKUNBLOCKREQUEST']._serialized_end=940
  _globals['_BLOCKUNBLOCKRESPONSE']._serialized_start=942
  _globals['_BLOCKUNBLOCKRESPONSE']._serialized_end=981
  _globals['_PROFILEDATAREQUEST']._serialized_start=983
  _globals['_PROFILEDATAREQUEST']._serialized_end=1015
  _globals['_PROFILEDATARESPONSE']._serialized_start=1018
  _globals['_PROFILEDATARESPONSE']._serialized_end=1174
  _globals['_PROFILEUPDATEREQUEST']._serialized_start=1177
  _globals['_PROFILEUPDATEREQUEST']._serialized_end=1334
  _globals['_PROFILEUPDATERESPONSE']._serialized_start=1336
  _globals['_PROFILEUPDATERESPONSE']._serialized_end=1391
  _globals['_GOOGLEUSERREQUEST']._serialized_start=1393
  _globals['_GOOGLEUSERREQUEST']._serialized_end=1446
  _globals['_GOOGLEUSERRESPONSE']._serialized_start=1448
  _globals['_GOOGLEUSERRESPONSE']._serialized_end=1525
  _globals['_FORGOTEEMAILREQUEST']._serialized_start=1527
  _globals['_FORGOTEEMAILREQUEST']._serialized_end=1563
  _globals['_FORGOTEEMAILRESPONSE']._serialized_start=1565
  _globals['_FORGOTEEMAILRESPONSE']._serialized_end=1604
  _globals['_CHANGEPASSWORDREQUEST']._serialized_start=1606
  _globals['_CHANGEPASSWORDREQUEST']._serialized_end=1662
  _globals['_CHANGEPASSWORDRESPONSE']._serialized_start=1664
  _globals['_CHANGEPASSWORDRESPONSE']._serialized_end=1705
  _globals['_POSTPROFILEREQUEST']._serialized_start=1707
  _globals['_POSTPROFILEREQUEST']._serialized_end=1744
  _globals['_POSTPROFILERESPONSE']._serialized_start=1746
  _globals['_POSTPROFILERESPONSE']._serialized_end=1790
  _globals['_POSTUNIQUEDATAREQUEST']._serialized_start=1792
  _globals['_POSTUNIQUEDATAREQUEST']._serialized_end=1832
  _globals['_POSTUNIQUEDATARESPONSE']._serialized_start=1834
  _globals['_POSTUNIQUEDATARESPONSE']._serialized_end=1931
  _globals['_COMMENTUNIQUEDATAREQUEST']._serialized_start=1933
  _globals['_COMMENTUNIQUEDATAREQUEST']._serialized_end=1976
  _globals['_COMMENTUNIQUEDATARESPONSE']._serialized_start=1978
  _globals['_COMMENTUNIQUEDATARESPONSE']._serialized_end=2046
  _globals['_USERSERVICE']._serialized_start=2049
  _globals['_USERSERVICE']._serialized_end=3405
# @@protoc_insertion_point(module_scope)
