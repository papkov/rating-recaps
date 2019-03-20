sed -e '$s/$//' -s ./collected_recaps/recaps_*.csv | cut --delimiter=";" -f9-10 --complement > merged_recaps.csv
iconv -f utf-8 -t windows-1251 merged_recaps.csv > merged_recaps_cp1251.csv