import dlYouTubeWhenThereAreDubbed as dl_vi_w_lang
import unittest


class OSEntryTestCase(unittest.TestCase):

  def setUp(self):
    self.ose = dl_vi_w_lang.OSEntry(
      folderpath='/dir1/subdir/thislevel',
      basefilename='this video [GypUQgXZmlQ].mp4',
      videoonly_or_audio_code=160
    )

  def test_1(self):
    ret_dot_ext = self.ose.dot_ext
    exp_dot_ext = '.mp4'
    self.assertEqual(exp_dot_ext, ret_dot_ext)
    ret_fsufix = self.ose.fsufix
    exp_fsufix = 'f160'
    self.assertEqual(exp_fsufix, ret_fsufix)
    ret_name = self.ose.name
    exp_name = 'this video [GypUQgXZmlQ]'
    self.assertEqual(exp_name, ret_name)
    ret_fn = self.ose.fn_as_name_ext
    exp_fn = 'this video [GypUQgXZmlQ].mp4'
    self.assertEqual(exp_fn, ret_fn)
    ret_fn = self.ose.get_fn_as_name_fsufix_ext_bksufix(3)
    exp_fn = 'this video [GypUQgXZmlQ].f160.mp4.bk3'
    self.assertEqual(exp_fn, ret_fn)
    ret_fn = self.ose.get_fp_for_fn_as_name_fsufix_ext_bksufix(3)
    exp_fn = '/dir1/subdir/thislevel/this video [GypUQgXZmlQ].f160.mp4.bk3'
    self.assertEqual(exp_fn, ret_fn)
    ret_ytid = self.ose.ytid
    exp_ytid = 'GypUQgXZmlQ'
    self.assertEqual(exp_ytid, ret_ytid)
