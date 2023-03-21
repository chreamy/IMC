p=[[1,0.5,1.45,0.75],[1.95,1,3.1,1.49],[0.67,0.31,1,0.48],[1.34,0.64,1.98,1]]

pw = p[0][1]
pb = p[0][2]
ps = p[0][3]
wp = p[1][0]
wb = p[1][2]
ws = p[1][3]
bp = p[2][0]
bw = p[2][1]
bs = p[2][3]
sp = p[3][0]
sw = p[3][1]
sb = p[3][2]

sbwps = sb*bw*wp*ps
sbpws = sb*bp*pw*ws
swbps = sw*wb*bp*ps
swpbs = sw*wp*pb*bs
spwbs = sp*pw*wb*bs
spbws = sp*pb*bw*ws
sbws = sb*bw*ws
sbps = sb*bp*ps
spws = sp*pw*ws
spbs = sp*pb*bs
swbs = sw*wb*bs
swps = sw*wp*ps
sps = sp*ps
sbs = sb*bs
sws = sw*ws
wpbw = wp*pb*bw
wspw = ws*sp*pw
wbpw = wb*bp*pw
wpsw = wp*ps*sw
wsbw = ws*sb*bw
wbsw = wb*bs*sw
wpw = wp*pw
wsw = ws*sw
wbw = wb*bw
pbwp = pb*bw*wp
psbp = ps*sb*bp
pwsp = pw*ws*sp
pbsp = pb*bs*sp
pswp = ps*sw*wp
pwbp = pw*wb*bp
pbp = pb*bp
psp = ps*sp
pwp = pw*wp
bpsb = bp*pb
bwsb = bw*wb
bspb = bs*sb
bpwb = bp*pb
bwpb = bw*wb
bswb = bs*sb
bpb = bp*pb
bwb = bw*wb
bsb = bs*sb
print('sbwps',sbwps,'sbpws',sbpws,'swbps',swbps,'swpbs',swpbs,'spwbs',spwbs,'spbws',spbws,'sbws',sbws,'sbps',sbps,'spws',spws,'spbs',spbs,'swbs',swbs,'swps',swps,'sps',sps,'sbs',sbs,'sws',sws)
spsps = sp*ps*sp*ps
spwbps = sp*pw*wb*bp*ps
print(spwbps)
print(wpbw,wspw,wbpw,wpsw ,wsbw ,wbsw )
print(pbwp,psbp,pwsp,pbsp,pswp,pwbp)
