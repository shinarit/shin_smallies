import sys

karakterek = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

szam = dict(zip(karakterek, range(len(karakterek))))

def calc(num, base):
  val = 0.0
  cbase = 1
  for n in reversed(num):
    val += szam[n] * cbase
    cbase = cbase * base
  return val

num = sys.argv[1]
dec = int(sys.argv[2])
min = 2.0
for n in num:
  if szam[n] > min:
    min = float(szam[n])

min = float(min)
max = float(len(karakterek) - 2)
if min < max:
  base = (min + max) / 2.0

  diff = calc(num, base)
  print "diff: %d, dec: %d" % (diff, dec)

  steps = 0
  while abs(diff - dec) > 0.1:
    if diff > dec:
      max, base = base, (min + base) / 2.0
    else:
      min, base = base, (max + base) / 2.0
    diff = calc(num, base)
    print "diff: %f, min: %f, max: %f" % (diff, min, max)
    steps += 1

  print "%f in %d steps" % (base, steps)
