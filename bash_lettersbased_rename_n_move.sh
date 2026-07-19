# Enable auto-exporting
set -a  
# looking up local "ENVCLEANSPECSTR1" for renameCleanSpecifiedStr.py
source .env
# Disable auto-exporting
set +a
renamePrefix.py "d' " -e=mp4 -y
renameAudioDurationIncluder.py -y -e=mp4; renameYtDlpBracketConventionToFormer.py tf -y
renameCleanBeginning.py -e=mp4 -p=3 -y
renameCleanRegExp.py -e=mp4 -r="\[\w+\d*\]+" -y
renameCleanSpecifiedStr.py -e=mp4 -s="$ENVCLEANSPECSTR1" -y
# renameCleanSpecifiedStr.py -e=mp4 -s=" (360)" -y
renameReplace12.py -e=mp4 -s1="(240)" -s2="240p" -y
# moveFilesDashedNameToCapSepNamesDir.py
