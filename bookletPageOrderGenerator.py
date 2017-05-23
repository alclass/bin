#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Explanation:
  This script generates the page ordering for creating a booklet
  in a 2-up strategy.

  E.g.:

    The page ordering for 8 pages is:
	=================================
    [8, 1, 2, 7, 6, 3, 4, 5]
	The 1st sheet will have pages 8 & 1 on front side, and 2 & 7 on back side.
	The 2nd sheet will have pages 6 & 3 on front side, and 4 & 5 on back side.
	The 2 sheets folded and centeredly stapled will form a booklet.

    The page ordering for 16 pages is:
	==================================
    [16, 1, 2, 15, 14, 3, 4, 13, 12, 5, 6, 11, 10, 7, 8, 9]
	The same observation as above.

	These results show the ordering to tell the printer the page sequence
	so that the 2-up both-sides sheets may form a booklet.
'''
import  codecs, os, sys


def process(lastpage, ongoingpage, orderlist):
  '''
  This is a recursive function. It uses the recursive lastpage and ongoingpage
  and stores the ordering in the orderlist.
  '''
  if ongoingpage > lastpage:
    raise ValueError('ongoingpage=%d > lastpage=%d :: this is against the logic here.' %(ongoingpage, lastpage))
  orderlist.append(lastpage)
  orderlist.append(ongoingpage)
  orderlist.append(ongoingpage+1)
  orderlist.append(lastpage - 1)
  lastpage = lastpage - 2
  ongoingpage = ongoingpage + 2
  if ongoingpage + 2 > lastpage:
    return orderlist
  return process(lastpage, ongoingpage, orderlist)


if __name__ == '__main__':
  '''
  The sys.argv input is, for the time being, unprotected. A TO-DO for the future to improve this.
  '''
  lastpage = int(sys.argv[1])
  if lastpage % 4 != 0:
    print ('n of pages should be multiple of 4')
    sys.exit(1)
  orderlist = process(lastpage, 1, [])
  print (orderlist)
