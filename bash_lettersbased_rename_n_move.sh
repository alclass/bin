renamePrefix.py "d' " -e=mp4 -y
renameAudioDurationIncluder.py -y -e=mp4; renameYtDlpBracketConventionToFormer.py tf -y
renameCleanBeginning.py -e=mp4 -p=3 -y
renameCleanRegExp.py -e=mp4 -r="\[\w+\d*\]+" -y
renameCleanSpecifiedStr.py -e=mp4 -s="RNER.COM - " -y
renameCleanSpecifiedStr.py -e=mp4 -s=" (360)" -y
# moveFilesDashedNameToCapSepNamesDir.py
