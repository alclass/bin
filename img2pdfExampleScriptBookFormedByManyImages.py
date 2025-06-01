import img2pdf, glob, os

input_path    = r'C:\Users\UP15\Documents\Bks\Sci Bks tmp\Phys Bks\Quantum Phys Bks\Heisenberg-PhysicsPhilosophy_jp2'
output_path   = r'C:\Users\UP15\Documents\Bks\Sci Bks tmp\Phys Bks\Quantum Phys Bks'
booksfilename = 'Heisenberg-PhysicsPhilosophy.pdf'
output_pdf_path = os.path.join(output_path, booksfilename)
print ('input jp2 @', input_path)
print ('output_pdf_path = ', output_pdf_path)

input_files = []
os.chdir(input_path)
jp2files = glob.glob('*.jp2') # jpeg2 input files
sorted(jp2files)
for eachFile in jp2files:
  filepath = os.path.join(input_path, eachFile)
  input_files.append(filepath)

# multiple inputs (variant 2)
a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
layout_fun = img2pdf.get_layout_fun(a4inpt)
print ('please wait: processing...')
# notice the output path will be the one changed above with os.chdir(path)
with open(booksfilename, 'wb') as f:
  f.write(img2pdf.convert(input_files, layout_fun=layout_fun))
print('Finished.')
