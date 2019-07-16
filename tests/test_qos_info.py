# -*- coding: utf-8 -*-

from .common import *
from oss2.models import UserQosInfo, BucketQosInfo

class TestQosInfo(OssTestCase):
    def test_get_user_qos_info(self):
        service = oss2.Service(oss2.Auth(OSS_ID, OSS_SECRET), OSS_ENDPOINT)
        result = service.get_user_qos_info()
        self.assertEqual(result.status, 200)

    def test_put_bucket_qos_info_with_all_args(self):
        # test put bucket qos info
        bucket_qos_info = BucketQosInfo(
                    total_upload_bw = 2,
                    intranet_upload_bw = 2,
                    extranet_upload_bw = 2,
                    total_download_bw = 2,
                    intranet_download_bw = 2,
                    extranet_download_bw = 2,
                    total_qps = -1,
                    intranet_qps = -1,
                    extranet_qps = -1)

        result = self.bucket.put_bucket_qos_info(bucket_qos_info)
        self.assertEqual(result.status, 200)

        result = self.bucket.get_bucket_qos_info()
        self.assertEqual(result.status, 200)
        self.assertEqual(result.total_upload_bw, bucket_qos_info.total_upload_bw)
        self.assertEqual(result.intranet_upload_bw, bucket_qos_info.intranet_upload_bw)
        self.assertEqual(result.extranet_upload_bw, bucket_qos_info.extranet_upload_bw)
        self.assertEqual(result.total_download_bw, bucket_qos_info.total_download_bw)
        self.assertEqual(result.intranet_download_bw, bucket_qos_info.intranet_download_bw)
        self.assertEqual(result.extranet_download_bw, bucket_qos_info.extranet_download_bw)
        self.assertEqual(result.total_qps, bucket_qos_info.total_qps)
        self.assertEqual(result.intranet_qps, bucket_qos_info.intranet_qps)
        self.assertEqual(result.extranet_qps, bucket_qos_info.extranet_qps)

        result = self.bucket.delete_bucket_qos_info()
        self.assertEqual(result.status, 204)

    def test_put_bucket_qos_info_with_none_args(self):
        # bucket qos info without setting
        bucket_qos_info = BucketQosInfo()

        # put bucket qos info without args, it would return default setting -1
        result = self.bucket.put_bucket_qos_info(bucket_qos_info)
        self.assertEqual(result.status, 200)

        result = self.bucket.get_bucket_qos_info()
        self.assertEqual(result.status, 200)
        self.assertEqual(result.total_upload_bw, -1)
        self.assertEqual(result.intranet_upload_bw, -1)
        self.assertEqual(result.extranet_upload_bw, -1)
        self.assertEqual(result.total_download_bw, -1)
        self.assertEqual(result.intranet_download_bw, -1)
        self.assertEqual(result.extranet_download_bw, -1)
        self.assertEqual(result.total_qps, -1)
        self.assertEqual(result.intranet_qps, -1)
        self.assertEqual(result.extranet_qps, -1)

        result = self.bucket.delete_bucket_qos_info()
        self.assertEqual(result.status, 204)

    def test_put_bucket_qos_info_illegal_args(self):
        service = oss2.Service(oss2.Auth(OSS_ID, OSS_SECRET), OSS_ENDPOINT)
        user_qos_info = service.get_user_qos_info()
        self.assertTrue(user_qos_info.total_upload_bw > 0, 'user_qos_info.total_upload_bw should be > 0')

        # test upload bw args
        # total_upload_bw > user_qos_info.total_upload_bw, should be failed.
        bw = user_qos_info.total_upload_bw + 1
        bucket_qos_info = BucketQosInfo(total_upload_bw=bw)
        self.assertRaises(oss2.exceptions.InvalidArgument, self.bucket.put_bucket_qos_info, bucket_qos_info)

        # total_upload_bw == user_qos_info.total_upload_bw, should be successful
        legal_total_upload_bw = user_qos_info.total_upload_bw
        bucket_qos_info = BucketQosInfo(total_upload_bw=legal_total_upload_bw)
        result = self.bucket.put_bucket_qos_info(bucket_qos_info)
        self.assertEqual(result.status, 200)

        # intranet_upload_bw > total_upload_bw, should be failed.
        bw = legal_total_upload_bw + 1
        bucket_qos_info = BucketQosInfo(intranet_upload_bw=bw)
        self.assertRaises(oss2.exceptions.InvalidArgument, self.bucket.put_bucket_qos_info, bucket_qos_info)

        # extranet_upload_bw > total_upload_bw, should be failed.
        bw = legal_total_upload_bw + 1
        bucket_qos_info = BucketQosInfo(extranet_upload_bw=bw)
        self.assertRaises(oss2.exceptions.InvalidArgument, self.bucket.put_bucket_qos_info, bucket_qos_info)

        # test download bw args
        # total_download_bw > user_qos_info.total_upload_bw, should be failed.
        bw = user_qos_info.total_download_bw + 1
        bucket_qos_info = BucketQosInfo(total_download_bw=bw)
        self.assertRaises(oss2.exceptions.InvalidArgument, self.bucket.put_bucket_qos_info, bucket_qos_info)

        # total_upload_bw == user_qos_info.total_upload_bw, should be successful
        legal_total_download_bw = user_qos_info.total_download_bw
        bucket_qos_info = BucketQosInfo(total_download_bw=legal_total_download_bw)
        result = self.bucket.put_bucket_qos_info(bucket_qos_info)
        self.assertEqual(result.status, 200)

        # intranet_download_bw > total_download_bw, should be failed.
        bw = legal_total_upload_bw + 1
        bucket_qos_info = BucketQosInfo(intranet_download_bw=bw)
        self.assertRaises(oss2.exceptions.InvalidArgument, self.bucket.put_bucket_qos_info, bucket_qos_info)

        # extranet_upload_bw > total_upload_bw, should be failed.
        bw = legal_total_download_bw + 1
        bucket_qos_info = BucketQosInfo(extranet_download_bw=bw)
        self.assertRaises(oss2.exceptions.InvalidArgument, self.bucket.put_bucket_qos_info, bucket_qos_info)

        # test qps args
        # total_qps > user_qos_info.total_qps, should be failed.
        qps = user_qos_info.total_qps + 1
        bucket_qos_info = BucketQosInfo(total_qps=qps)
        self.assertRaises(oss2.exceptions.InvalidArgument, self.bucket.put_bucket_qos_info, bucket_qos_info)

        # total_qps == user_qos_info.total_qps, should be successful
        legal_total_qps = user_qos_info.total_qps
        bucket_qos_info = BucketQosInfo(total_qps=legal_total_qps)
        result = self.bucket.put_bucket_qos_info(bucket_qos_info)
        self.assertEqual(result.status, 200)

        # intranet_qps > total_qps, should be failed.
        qps = legal_total_qps + 1
        bucket_qos_info = BucketQosInfo(intranet_qps=qps)
        self.assertRaises(oss2.exceptions.InvalidArgument, self.bucket.put_bucket_qos_info, bucket_qos_info)

        # extranet_qps > total_qps, should be failed.
        qps = legal_total_qps + 1
        bucket_qos_info = BucketQosInfo(extranet_qps=qps)
        self.assertRaises(oss2.exceptions.InvalidArgument, self.bucket.put_bucket_qos_info, bucket_qos_info)

    # def test_forbid_upload(self):
    #     key = 'bucket-qos-info-test-forbid-upload-object'
    #     content = '123'

    #     try:
    #         # Before bucket qos info setting
    #         result = self.bucket.put_object(key, content)
    #         self.assertEqual(result.status, 200)

    #         bucket_qos_info = BucketQosInfo(extranet_upload_bw=0)
    #         result = self.bucket.put_bucket_qos_info(bucket_qos_info)
    #         self.assertEqual(result.status, 200)

    #         result = self.bucket.get_bucket_qos_info()
    #         self.assertEqual(result.extranet_upload_bw, 0)

    #         # After bucket qos info setting, it should be failed.
    #         self.assertRaises(oss2.exceptions.ServerError, self.bucket.put_object, key, content)
    #     finally:
    #         result = self.bucket.delete_bucket_qos_info()
    #         self.assertEqual(result.status, 204)

if __name__ == '__main__':
    unittest.main()