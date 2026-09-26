```
male CNS bank builder; registration docs/plans/2026-09-25-male-cns-bank-builder-registration.md, revision 2.1
git head e0a3cd744c39903bcdcbb218c10eafa3ed1b048c; tree under results/genome/c6/ and docs/plans/: clean
builder sha256 (LF) a29cf45825271e32019d6441b276a351479dea5788360d223e245e3ac451b2ca; registration sha256 (LF) 5bcb4bc00bd6357ab50db196dcc727e8ac0ea73497050e2a569aba35c1a9dbf2
builder_environment (section 10.4; not the instrument's environment (tools/.venv: python 3.10.20, numpy 2.2.6), which this builder does not use): {'python': '3.13.14', 'numpy': '2.5.3', 'pandas': '3.0.6', 'pyarrow': '25.0.1', 'psutil': '7.2.2'}; compared with the pins: python, numpy, pandas, pyarrow; psutil reported, not compared
pins: flyvis-65 CSVs and both Janelia files equal section 1.1
  results/genome/bank/offsets.csv: sha256 (LF) 8c45e8508d8f6ae45e9ab3f9d95d58e4521894ccfa51954f6d77d41e550fa5f0
  results/genome/bank/types.csv: sha256 (LF) 237a195a36f62ce182fee8486394c27d2beb9825bc029cb215c39c0fa323a477
  body-annotations-male-cns-v1.0-minconf-0.5.feather: 14483314 bytes, sha256 2177e246113e4cfbf1e7772ec37c6da1955ff22e8063d0b1f833101f99a9a3b2, downloaded 2026-09-23 UTC
  connectome-weights-male-cns-v1.0-minconf-0.5.feather: 1051241946 bytes, sha256 e35da783d1c686b2b58b3b87cd6a403ae43bfcfba8bff28e08ef752c1a56afc1, downloaded 2026-09-23 UTC
weight file: schema ['body_pre: int64', 'body_post: int64', 'weight: int64']; 2318 record batches; pandas metadata stop 151856684; written by {'library': 'pyarrow', 'version': '19.0.1'}
  uncompressed int64 data would be 3644560416 bytes; the file is 1051241946 bytes
  body compression codec per record batch, from the flatbuffer headers only (no message body read): {'LZ4_FRAME': 2318}; footer blocks 2318 (reader: 2318); header row lengths sum to 151856684 (pandas stop 151856684); footer/header body-length mismatches 0
annotation file: body compression codec per record batch {'LZ4_FRAME': 4}; 4 record batches, 211577 rows in their headers
map: 61 flyvis names mapped, 55 placed; not placed: ['Mi3', 'Tm28', 'Mi12', 'CT1(Lo1)', 'R3', 'R2', 'R5', 'R4', 'R6', 'Mi11']
density targets (section 5.3; placed grid 55 types, |Omega| = 2961 outside cells):
  pooled             {'omega': 2961, 'present': 511, 'T': 0.172577, 'K': 1022}; registered {'omega': 2961, 'present': 511, 'T': 0.172577, 'K': 1022} <- registered (D15)
  restrict           {'omega': 2961, 'present': 497, 'T': 0.167849, 'K': 994}; registered {'omega': 2961, 'present': 497, 'T': 0.167849, 'K': 994}
  full_grid_b_prime  {'omega_full': 4161, 'present_full': 572, 'T': 0.137467, 'K': 814}; registered {'omega_full': 4161, 'present_full': 572, 'T': 0.137467, 'K': 814}
annotations: 211577 rows, 36 columns
special-case strings in the name columns (section 3.2; body counts, all sides):
  type: {'Am1': 2, 'CT1': 2, 'R1-R6': 3377, 'R7R8_unclear': 85, 'R7_unclear': 404, 'R7d': 82, 'R7p': 332, 'R7y': 482, 'R8_unclear': 442, 'R8d': 76, 'R8p': 330, 'R8y': 481, 'TmY9a': 471, 'TmY9b': 515}
  flywireType: {'Am1': 2, 'CT1': 2, 'R1-6': 3377, 'R7': 1300, 'R8': 1329, 'TmY9q': 515, 'TmY9q__perp': 471}
  absent Mi3: bodies by column {'type': 0, 'flywireType': 0}
  absent Mi11: bodies by column {'type': 0, 'flywireType': 0}
  absent Mi12: bodies by column {'type': 0, 'flywireType': 0}
  absent Tm28: bodies by column {'type': 0, 'flywireType': 0}

type map as applied (section 3.2). L, R: bodies per lobe after the side rule and the flip. side rule: [L, R] per step that assigned the side (before the flip). under type / flywireType: all bodies whose column equals the mapped string, per lobe. disagree: bodies where either column equals it and the two columns differ
  Tm5Y      <- type='Tm5Y': L 435, R 463; side rule {'somaSide': [435, 463], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [435, 463], under flywireType [0, 0]; disagree 898; assignedOlHex1 non-null 0; status {'Traced': 898}
  T4d       <- type='T4d': L 850, R 859; side rule {'somaSide': [850, 859], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [850, 859], under flywireType [850, 860]; disagree 1; assignedOlHex1 non-null 0; status {'Traced': 1709}
  Tm2       <- type='Tm2': L 883, R 883; side rule {'somaSide': [883, 883], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [883, 883], under flywireType [883, 883]; disagree 0; assignedOlHex1 non-null 1758; status {'Traced': 1766}
  TmY15     <- type='TmY15': L 99, R 110; side rule {'somaSide': [99, 110], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [99, 110], under flywireType [99, 110]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 209}
  Tm3       <- type='Tm3': L 1017, R 1037; side rule {'somaSide': [1017, 1037], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [1017, 1037], under flywireType [1017, 1037]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 2054}
  Tm5c      <- type='Tm5c': L 376, R 374; side rule {'somaSide': [376, 374], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [376, 374], under flywireType [376, 374]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 750}
  Lawf1     <- type='Lawf1': L 177, R 184; side rule {'somaSide': [177, 184], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [177, 184], under flywireType [177, 184]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 361}
  TmY14     <- type='TmY14': L 243, R 234; side rule {'somaSide': [243, 234], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [243, 234], under flywireType [243, 234]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 477}
  T2        <- type='T2': L 808, R 822; side rule {'somaSide': [808, 822], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [808, 822], under flywireType [808, 822]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 1630}
  L2        <- type='L2': L 886, R 893; side rule {'somaSide': [886, 893], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [886, 893], under flywireType [886, 893]; disagree 0; assignedOlHex1 non-null 1767; status {'Traced': 1779}
  Lawf2     <- type='Lawf2': L 195, R 188; side rule {'somaSide': [195, 188], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [195, 188], under flywireType [195, 188]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 383}
  T4c       <- type='T4c': L 895, R 883; side rule {'somaSide': [895, 883], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [895, 883], under flywireType [895, 883]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 1778}
  TmY5a     <- type='TmY5a': L 686, R 678; side rule {'somaSide': [686, 678], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [686, 678], under flywireType [686, 678]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 1364}
  T3        <- type='T3': L 964, R 976; side rule {'somaSide': [964, 976], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [964, 976], under flywireType [964, 976]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 1940}
  T5b       <- type='T5b': L 863, R 852; side rule {'somaSide': [863, 852], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [863, 852], under flywireType [863, 852]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 1715}
  T5c       <- type='T5c': L 862, R 858; side rule {'somaSide': [862, 858], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [862, 858], under flywireType [862, 858]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 1720}
  Mi15      <- type='Mi15': L 569, R 582; side rule {'somaSide': [569, 582], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [569, 582], under flywireType [569, 582]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 1151}
  Tm20      <- type='Tm20': L 886, R 876; side rule {'somaSide': [886, 876], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [886, 876], under flywireType [886, 876]; disagree 0; assignedOlHex1 non-null 1732; status {'Traced': 1762}
  Mi10      <- type='Mi10': L 222, R 222; side rule {'somaSide': [222, 222], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [222, 222], under flywireType [222, 222]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 444}
  Tm5b      <- type='Tm5b': L 260, R 262; side rule {'somaSide': [260, 262], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [260, 262], under flywireType [260, 262]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 522}
  TmY3      <- type='TmY3': L 415, R 409; side rule {'somaSide': [415, 409], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [415, 409], under flywireType [415, 409]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 824}
  C3        <- type='C3': L 887, R 892; side rule {'somaSide': [887, 892], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [887, 892], under flywireType [887, 892]; disagree 0; assignedOlHex1 non-null 1770; status {'Traced': 1779}
  CT1(M10)  <- type='CT1' FLIP carries ['CT1(M10)', 'CT1(Lo1)']: L 1, R 1; side rule {'somaSide': [1, 1], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [1, 1], under flywireType [1, 1]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 2}
  Tm1       <- type='Tm1': L 887, R 890; side rule {'somaSide': [887, 890], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [887, 890], under flywireType [887, 890]; disagree 0; assignedOlHex1 non-null 1767; status {'Traced': 1777}
  Mi9       <- type='Mi9': L 886, R 889; side rule {'somaSide': [886, 889], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [886, 889], under flywireType [886, 889]; disagree 0; assignedOlHex1 non-null 1760; status {'Traced': 1775}
  Tm16      <- type='Tm16': L 199, R 197; side rule {'somaSide': [199, 197], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [199, 197], under flywireType [199, 197]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 396}
  TmY9      <- flywireType='TmY9q': L 249, R 266; side rule {'somaSide': [249, 266], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [0, 0], under flywireType [249, 266]; disagree 515; assignedOlHex1 non-null 0; status {'Traced': 515}
  L4        <- type='L4': L 879, R 891; side rule {'somaSide': [879, 891], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [879, 891], under flywireType [879, 891]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 1769, 'null': 1}
  Mi4       <- type='Mi4': L 883, R 889; side rule {'somaSide': [883, 889], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [883, 889], under flywireType [883, 889]; disagree 0; assignedOlHex1 non-null 1758; status {'Traced': 1772}
  T1        <- type='T1': L 885, R 892; side rule {'somaSide': [885, 892], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [885, 892], under flywireType [885, 892]; disagree 0; assignedOlHex1 non-null 1764; status {'Traced': 1777}
  Mi13      <- type='Mi13': L 457, R 453; side rule {'somaSide': [457, 453], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [457, 453], under flywireType [457, 453]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 910}
  TmY4      <- type='TmY4': L 274, R 288; side rule {'somaSide': [274, 288], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [274, 288], under flywireType [274, 288]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 562}
  R8        <- flywireType='R8': L 625, R 704; side rule {'somaSide': [14, 0], 'rootSide': [611, 704], 'instance': [0, 0], 'unassigned': 0}; under type [0, 0], under flywireType [625, 704]; disagree 1329; assignedOlHex1 non-null 0; status {'Traced': 1329}
  Mi2       <- type='Mi2': L 494, R 492; side rule {'somaSide': [494, 492], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [494, 492], under flywireType [494, 492]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 986}
  T4b       <- type='T4b': L 844, R 846; side rule {'somaSide': [844, 846], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [844, 846], under flywireType [844, 846]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 1690}
  Tm4       <- type='Tm4': L 837, R 833; side rule {'somaSide': [837, 833], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [837, 833], under flywireType [837, 833]; disagree 0; assignedOlHex1 non-null 833; status {'Traced': 1670}
  R1        <- type='R1-R6' carries ['R1', 'R3', 'R2', 'R5', 'R4', 'R6']: L 1112, R 2265; side rule {'somaSide': [4, 9], 'rootSide': [1108, 2256], 'instance': [0, 0], 'unassigned': 0}; under type [1112, 2265], under flywireType [0, 0]; disagree 3377; assignedOlHex1 non-null 0; status {'Traced': 1394, 'null': 1983}
  T5a       <- type='T5a': L 826, R 838; side rule {'somaSide': [826, 838], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [826, 838], under flywireType [826, 838]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 1664}
  T4a       <- type='T4a': L 835, R 849; side rule {'somaSide': [835, 849], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [835, 849], under flywireType [835, 849]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 1684}
  C2        <- type='C2': L 871, R 874; side rule {'somaSide': [871, 874], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [871, 874], under flywireType [871, 874]; disagree 0; assignedOlHex1 non-null 874; status {'Traced': 1745}
  L1        <- type='L1': L 884, R 892; side rule {'somaSide': [884, 892], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [884, 892], under flywireType [884, 892]; disagree 0; assignedOlHex1 non-null 1767; status {'Traced': 1776}
  Am        <- type='Am1': L 1, R 1; side rule {'somaSide': [1, 1], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [1, 1], under flywireType [1, 1]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 2}
  Mi1       <- type='Mi1': L 886, R 887; side rule {'somaSide': [886, 887], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [886, 887], under flywireType [886, 887]; disagree 0; assignedOlHex1 non-null 1762; status {'Traced': 1773}
  Mi14      <- type='Mi14': L 160, R 155; side rule {'somaSide': [160, 155], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [160, 155], under flywireType [160, 155]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 315}
  L5        <- type='L5': L 889, R 898; side rule {'somaSide': [889, 898], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [889, 898], under flywireType [890, 898]; disagree 1; assignedOlHex1 non-null 1773; status {'Traced': 1787}
  Tm9       <- type='Tm9': L 884, R 887; side rule {'somaSide': [884, 887], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [884, 887], under flywireType [884, 887]; disagree 0; assignedOlHex1 non-null 1743; status {'Traced': 1771}
  TmY10     <- type='TmY10': L 274, R 278; side rule {'somaSide': [274, 278], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [274, 278], under flywireType [274, 278]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 552}
  TmY18     <- type='TmY18': L 673, R 694; side rule {'somaSide': [673, 694], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [673, 694], under flywireType [0, 0]; disagree 1367; assignedOlHex1 non-null 0; status {'Traced': 1367}
  Tm5a      <- type='Tm5a': L 317, R 307; side rule {'somaSide': [317, 307], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [317, 307], under flywireType [317, 307]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 624}
  T2a       <- type='T2a': L 933, R 939; side rule {'somaSide': [933, 939], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [933, 939], under flywireType [933, 939]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 1872}
  TmY13     <- type='TmY13': L 221, R 211; side rule {'somaSide': [221, 211], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [221, 211], under flywireType [0, 0]; disagree 432; assignedOlHex1 non-null 0; status {'Traced': 432}
  R7        <- flywireType='R7': L 608, R 692; side rule {'somaSide': [1, 1], 'rootSide': [607, 691], 'instance': [0, 0], 'unassigned': 0}; under type [0, 0], under flywireType [608, 692]; disagree 1300; assignedOlHex1 non-null 0; status {'Anchor': 1, 'Traced': 1299}
  T5d       <- type='T5d': L 812, R 808; side rule {'somaSide': [812, 808], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [812, 808], under flywireType [812, 808]; disagree 0; assignedOlHex1 non-null 0; status {'Traced': 1620}
  Tm30      <- type='Tm30': L 63, R 61; side rule {'somaSide': [63, 61], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [63, 61], under flywireType [0, 0]; disagree 124; assignedOlHex1 non-null 0; status {'Traced': 124}
  L3        <- type='L3': L 880, R 892; side rule {'somaSide': [880, 892], 'rootSide': [0, 0], 'instance': [0, 0], 'unassigned': 0}; under type [880, 892], under flywireType [880, 892]; disagree 0; assignedOlHex1 non-null 892; status {'Traced': 1772}
the two name columns where they disagree (section 3.1; bodies where either column equals the mapped string; a different spelling of one object shows here, not as an absence):
  Tm5Y      {"type='Tm5Y' / flywireType='Tm5f'": 898}
  T4d       {"type='T4_unclear' / flywireType='T4d'": 1}
  TmY9      {"type='TmY9b' / flywireType='TmY9q'": 515}
  R8        {"type='R8_unclear' / flywireType='R8'": 442, "type='R8d' / flywireType='R8'": 76, "type='R8p' / flywireType='R8'": 330, "type='R8y' / flywireType='R8'": 481}
  R1        {"type='R1-R6' / flywireType='R1-6'": 3377}
  L5        {"type=None / flywireType='L5'": 1}
  TmY18     {"type='TmY18' / flywireType='Tm27'": 1367}
  TmY13     {"type='TmY13' / flywireType='TmY11'": 432}
  R7        {"type='R7_unclear' / flywireType='R7'": 404, "type='R7d' / flywireType='R7'": 82, "type='R7p' / flywireType='R7'": 332, "type='R7y' / flywireType='R7'": 482}
  Tm30      {"type='Tm30' / flywireType='Tm31'": 124}
status per lobe, [L, R] after the side rule and the flip (types with any status other than Traced):
  L4        {'Traced': [878, 891], 'null': [1, 0]}
  R1        {'Traced': [501, 893], 'null': [611, 1372]}
  R7        {'Anchor': [1, 0], 'Traced': [607, 692]}
placed types: 55; mapped flyvis names: 61
self-test of the map (section 3.3): ZERO NAME MATCHES, MAP STRING NOT FOUND, BODY IN TWO TYPES, TYPE WITH NO CELLS: all pass

whole file, status x side under the registered side rule of section 4 (all 211577 bodies, before any flip) [L, R, unassigned]:
  Anchor       [137, 63, 411]
  Assign       [1, 0, 1831]
  Glia         [0, 0, 11864]
  Orphan       [1390, 686, 13849]
  Traced       [81378, 82753, 991]
  Unimportant  [0, 0, 10751]
  null         [854, 1985, 2633]
  Traced, somaSide then rootSide only (the instance step left out): L 81362, R 82738
R7/R8 sides from the `type` variants, independent of flywireType (section 4; R7R8_unclear split by its flywireType):
  R7R8_unclear: 85 bodies, flywireType {'None': 85}
  R7: type variants {'R7d': 82, 'R7p': 332, 'R7y': 482, 'R7_unclear': 404}; sides [L, R] [608, 692]; the same bodies as flywireType='R7': True (symmetric difference 0)
  R8: type variants {'R8d': 76, 'R8p': 330, 'R8y': 481, 'R8_unclear': 442}; sides [L, R] [625, 704]; the same bodies as flywireType='R8': True (symmetric difference 0)
two spellings of one object (section 3.1):
  type='R1-R6': 3377 bodies; flywireType='R1-6': 3377 bodies; the same bodyIds: True (symmetric difference 0)

weight pass: 69503 placed bodies with a lobe
  rows read 151856684 (metadata stop 151856684); batches 2318 of 2318; autapse rows dropped 2
  outside rows kept: same lobe 2332880, across lobes 0; duplicate outside keys 0; cross-lobe weight of outside type pairs 0

lobe consistency (section 4; outside-block type pairs only): same-lobe share of each placed type's weight, as source and target together (as source / as target); the inconsistencies: neuron-pair rows whose partner is in the other lobe, of all rows, as source and as target, and their weight
  Tm5Y      1.0000 (1.0000 / 1.0000); cross-lobe rows 0/25214 as source, 0/48026 as target; cross-lobe weight 0 of 199399
  T4d       1.0000 (1.0000 / 1.0000); cross-lobe rows 0/45614 as source, 0/39115 as target; cross-lobe weight 0 of 201776
  Tm2       1.0000 (1.0000 / 1.0000); cross-lobe rows 0/72070 as source, 0/41599 as target; cross-lobe weight 0 of 710392
  TmY15     1.0000 (1.0000 / 1.0000); cross-lobe rows 0/64456 as source, 0/53537 as target; cross-lobe weight 0 of 467621
  Tm3       1.0000 (1.0000 / 1.0000); cross-lobe rows 0/129360 as source, 0/107556 as target; cross-lobe weight 0 of 1169044
  Tm5c      1.0000 (1.0000 / 1.0000); cross-lobe rows 0/27010 as source, 0/25202 as target; cross-lobe weight 0 of 170504
  Lawf1     1.0000 (1.0000 / 1.0000); cross-lobe rows 0/18447 as source, 0/29210 as target; cross-lobe weight 0 of 137397
  TmY14     1.0000 (1.0000 / 1.0000); cross-lobe rows 0/15217 as source, 0/65917 as target; cross-lobe weight 0 of 384650
  T2        1.0000 (1.0000 / 1.0000); cross-lobe rows 0/55760 as source, 0/124988 as target; cross-lobe weight 0 of 657782
  L2        1.0000 (1.0000 / 1.0000); cross-lobe rows 0/42465 as source, 0/22007 as target; cross-lobe weight 0 of 1233848
  Lawf2     1.0000 (1.0000 / 1.0000); cross-lobe rows 0/3036 as source, 0/34399 as target; cross-lobe weight 0 of 79577
  T4c       1.0000 (1.0000 / 1.0000); cross-lobe rows 0/54766 as source, 0/41117 as target; cross-lobe weight 0 of 230259
  TmY5a     1.0000 (1.0000 / 1.0000); cross-lobe rows 0/42825 as source, 0/123477 as target; cross-lobe weight 0 of 579013
  T3        1.0000 (1.0000 / 1.0000); cross-lobe rows 0/23451 as source, 0/41835 as target; cross-lobe weight 0 of 342229
  T5b       1.0000 (1.0000 / 1.0000); cross-lobe rows 0/51052 as source, 0/36221 as target; cross-lobe weight 0 of 265488
  T5c       1.0000 (1.0000 / 1.0000); cross-lobe rows 0/47859 as source, 0/33536 as target; cross-lobe weight 0 of 192460
  Mi15      1.0000 (1.0000 / 1.0000); cross-lobe rows 0/24372 as source, 0/22752 as target; cross-lobe weight 0 of 145746
  Tm20      1.0000 (1.0000 / 1.0000); cross-lobe rows 0/44219 as source, 0/53236 as target; cross-lobe weight 0 of 371482
  Mi10      1.0000 (1.0000 / 1.0000); cross-lobe rows 0/39256 as source, 0/25569 as target; cross-lobe weight 0 of 203784
  Tm5b      1.0000 (1.0000 / 1.0000); cross-lobe rows 0/9993 as source, 0/19365 as target; cross-lobe weight 0 of 73852
  TmY3      1.0000 (1.0000 / 1.0000); cross-lobe rows 0/39335 as source, 0/97780 as target; cross-lobe weight 0 of 548972
  C3        1.0000 (1.0000 / 1.0000); cross-lobe rows 0/61809 as source, 0/46264 as target; cross-lobe weight 0 of 684155
  CT1(M10)  1.0000 (1.0000 / 1.0000); cross-lobe rows 0/18723 as source, 0/22296 as target; cross-lobe weight 0 of 403235  FLIP
  Tm1       1.0000 (1.0000 / 1.0000); cross-lobe rows 0/72118 as source, 0/42529 as target; cross-lobe weight 0 of 750445
  Mi9       1.0000 (1.0000 / 1.0000); cross-lobe rows 0/75297 as source, 0/61337 as target; cross-lobe weight 0 of 710381
  Tm16      1.0000 (1.0000 / 1.0000); cross-lobe rows 0/52838 as source, 0/33796 as target; cross-lobe weight 0 of 247979
  TmY9      1.0000 (1.0000 / 1.0000); cross-lobe rows 0/23445 as source, 0/43306 as target; cross-lobe weight 0 of 157569
  L4        1.0000 (1.0000 / 1.0000); cross-lobe rows 0/64605 as source, 0/21531 as target; cross-lobe weight 0 of 290619
  Mi4       1.0000 (1.0000 / 1.0000); cross-lobe rows 0/91439 as source, 0/66087 as target; cross-lobe weight 0 of 745027
  T1        1.0000 (1.0000 / 1.0000); cross-lobe rows 0/3521 as source, 0/16950 as target; cross-lobe weight 0 of 295188
  Mi13      1.0000 (1.0000 / 1.0000); cross-lobe rows 0/60091 as source, 0/25655 as target; cross-lobe weight 0 of 293421
  TmY4      1.0000 (1.0000 / 1.0000); cross-lobe rows 0/20453 as source, 0/67021 as target; cross-lobe weight 0 of 218310
  R8        1.0000 (1.0000 / 1.0000); cross-lobe rows 0/17209 as source, 0/3793 as target; cross-lobe weight 0 of 161146
  Mi2       1.0000 (1.0000 / 1.0000); cross-lobe rows 0/43715 as source, 0/39639 as target; cross-lobe weight 0 of 268084
  T4b       1.0000 (1.0000 / 1.0000); cross-lobe rows 0/57257 as source, 0/42481 as target; cross-lobe weight 0 of 280875
  Tm4       1.0000 (1.0000 / 1.0000); cross-lobe rows 0/92745 as source, 0/108881 as target; cross-lobe weight 0 of 935327
  R1        1.0000 (1.0000 / 1.0000); cross-lobe rows 0/14136 as source, 0/12991 as target; cross-lobe weight 0 of 270466
  T5a       1.0000 (1.0000 / 1.0000); cross-lobe rows 0/43506 as source, 0/28706 as target; cross-lobe weight 0 of 190556
  T4a       1.0000 (1.0000 / 1.0000); cross-lobe rows 0/52583 as source, 0/37587 as target; cross-lobe weight 0 of 220714
  C2        1.0000 (1.0000 / 1.0000); cross-lobe rows 0/30190 as source, 0/30846 as target; cross-lobe weight 0 of 363482
  L1        1.0000 (1.0000 / 1.0000); cross-lobe rows 0/26664 as source, 0/25297 as target; cross-lobe weight 0 of 879794
  Am        1.0000 (1.0000 / 1.0000); cross-lobe rows 0/16226 as source, 0/9046 as target; cross-lobe weight 0 of 161309
  Mi1       1.0000 (1.0000 / 1.0000); cross-lobe rows 0/110070 as source, 0/61366 as target; cross-lobe weight 0 of 1151809
  Mi14      1.0000 (1.0000 / 1.0000); cross-lobe rows 0/31827 as source, 0/27973 as target; cross-lobe weight 0 of 149460
  L5        1.0000 (1.0000 / 1.0000); cross-lobe rows 0/92100 as source, 0/35720 as target; cross-lobe weight 0 of 989171
  Tm9       1.0000 (1.0000 / 1.0000); cross-lobe rows 0/12673 as source, 0/38124 as target; cross-lobe weight 0 of 231978
  TmY10     1.0000 (1.0000 / 1.0000); cross-lobe rows 0/30481 as source, 0/32744 as target; cross-lobe weight 0 of 161470
  TmY18     1.0000 (1.0000 / 1.0000); cross-lobe rows 0/39838 as source, 0/81528 as target; cross-lobe weight 0 of 364329
  Tm5a      1.0000 (1.0000 / 1.0000); cross-lobe rows 0/8948 as source, 0/17161 as target; cross-lobe weight 0 of 72648
  T2a       1.0000 (1.0000 / 1.0000); cross-lobe rows 0/48531 as source, 0/70565 as target; cross-lobe weight 0 of 408732
  TmY13     1.0000 (1.0000 / 1.0000); cross-lobe rows 0/25788 as source, 0/39220 as target; cross-lobe weight 0 of 232764
  R7        1.0000 (1.0000 / 1.0000); cross-lobe rows 0/8859 as source, 0/3046 as target; cross-lobe weight 0 of 83325
  T5d       1.0000 (1.0000 / 1.0000); cross-lobe rows 0/45108 as source, 0/31289 as target; cross-lobe weight 0 of 189425
  Tm30      1.0000 (1.0000 / 1.0000); cross-lobe rows 0/2688 as source, 0/4882 as target; cross-lobe weight 0 of 17820
  L3        1.0000 (1.0000 / 1.0000); cross-lobe rows 0/61622 as source, 0/16779 as target; cross-lobe weight 0 of 470980
lobe consistency: every placed type >= 0.5 (FLIP applied)

the cut (section 5.2, D1 (b), D15 pooled): K = 1022; w_min = 1; c* = 2.994356659142212; pooled present 1022; tie excess 0; shortfall 0
  lobe L: present outside cells 496 of 2961, density 0.167511
  lobe R: present outside cells 526 of 2961, density 0.177643
  CT1(M10) (carries 2 flyvis names): present cells at c* in its row / column: lobe L 9 / 31 (1 bodies), lobe R 9 / 30 (1 bodies)
  R1 (carries 6 flyvis names): present cells at c* in its row / column: lobe L 3 / 1 (1112 bodies), lobe R 3 / 1 (2265 bodies)

diagnostics (section 5.4; decide nothing; outside block A only; |Omega| = 2961 per lobe)
  w_min = 1: c = 1 has rank 1526 of 5922 pooled outside values (values >= 1)
    c* (pooled collapse, registered)   c = 2.99436  lobe L: present 496, density 0.167511, inferable 64/64, mirrors 3, smallest endpoint keep T5a 4
    c* (pooled collapse, registered)   c = 2.99436  lobe R: present 526, density 0.177643, inferable 64/64, mirrors 3, smallest endpoint keep T5a 4
    c* (restrict-only collapse)        c = 3.27136  lobe L: present 481, density 0.162445, inferable 64/64, mirrors 2, smallest endpoint keep T4c 4
    c* (restrict-only collapse)        c = 3.27136  lobe R: present 513, density 0.173252, inferable 64/64, mirrors 2, smallest endpoint keep T5a 4
    c* (b', full-grid density)         c = 5.40206  lobe L: present 392, density 0.132388, inferable 64/64, mirrors 0, smallest endpoint keep Tm9 2
    c* (b', full-grid density)         c = 5.40206  lobe R: present 422, density 0.142519, inferable 64/64, mirrors 1, smallest endpoint keep T4c 3
    c*_L (left lobe alone)             c = 2.69453  lobe L: present 511, density 0.172577, inferable 64/64, mirrors 3, smallest endpoint keep T5a 4
    c*_L (left lobe alone)             c = 2.69453  lobe R: present 541, density 0.182709, inferable 64/64, mirrors 3, smallest endpoint keep T5a 4
    c*_R (right lobe alone)            c = 3.39337  lobe L: present 474, density 0.160081, inferable 64/64, mirrors 2, smallest endpoint keep T4c 4
    c*_R (right lobe alone)            c = 3.39337  lobe R: present 511, density 0.172577, inferable 64/64, mirrors 2, smallest endpoint keep T5a 4
    c = 0.5                            c = 0.5  lobe L: present 946, density 0.319487, inferable 64/64, mirrors 4, smallest endpoint keep T5a 8
    c = 0.5                            c = 0.5  lobe R: present 964, density 0.325566, inferable 64/64, mirrors 4, smallest endpoint keep T5a 8
    c = 1                              c = 1  lobe L: present 739, density 0.249578, inferable 64/64, mirrors 4, smallest endpoint keep T5a 6
    c = 1                              c = 1  lobe R: present 787, density 0.265789, inferable 64/64, mirrors 4, smallest endpoint keep T5a 6
    c = 2                              c = 2  lobe L: present 553, density 0.186761, inferable 64/64, mirrors 3, smallest endpoint keep T5a 4
    c = 2                              c = 2  lobe R: present 589, density 0.198919, inferable 64/64, mirrors 3, smallest endpoint keep T5a 4
  w_min = 2: c = 1 has rank 1189 of 5922 pooled outside values (values >= 1)
    c* (pooled collapse, registered)   c = 1.975  lobe L: present 496, density 0.167511, inferable 64/64, mirrors 3, smallest endpoint keep T5a 4
    c* (pooled collapse, registered)   c = 1.975  lobe R: present 526, density 0.177643, inferable 64/64, mirrors 3, smallest endpoint keep T5a 4
    c* (restrict-only collapse)        c = 2.075  lobe L: present 477, density 0.161094, inferable 64/64, mirrors 3, smallest endpoint keep Tm9 3
    c* (restrict-only collapse)        c = 2.075  lobe R: present 517, density 0.174603, inferable 64/64, mirrors 3, smallest endpoint keep T5a 4
    c* (b', full-grid density)         c = 3.91996  lobe L: present 389, density 0.131375, inferable 56/64, mirrors 1, smallest endpoint keep Tm9 1
    c* (b', full-grid density)         c = 3.91996  lobe R: present 425, density 0.143533, inferable 64/64, mirrors 1, smallest endpoint keep T4c 3
    c*_L (left lobe alone)             c = 1.8386  lobe L: present 511, density 0.172577, inferable 64/64, mirrors 3, smallest endpoint keep T5a 4
    c*_L (left lobe alone)             c = 1.8386  lobe R: present 534, density 0.180344, inferable 64/64, mirrors 3, smallest endpoint keep T5a 4
    c*_R (right lobe alone)            c = 2.24209  lobe L: present 469, density 0.158392, inferable 64/64, mirrors 3, smallest endpoint keep Tm9 3
    c*_R (right lobe alone)            c = 2.24209  lobe R: present 511, density 0.172577, inferable 64/64, mirrors 3, smallest endpoint keep T4a 4
    c = 0.5                            c = 0.5  lobe L: present 713, density 0.240797, inferable 64/64, mirrors 3, smallest endpoint keep T5a 5
    c = 0.5                            c = 0.5  lobe R: present 749, density 0.252955, inferable 64/64, mirrors 3, smallest endpoint keep T5a 4
    c = 1                              c = 1  lobe L: present 575, density 0.194191, inferable 64/64, mirrors 3, smallest endpoint keep T5a 4
    c = 1                              c = 1  lobe R: present 614, density 0.207362, inferable 64/64, mirrors 3, smallest endpoint keep T5a 4
    c = 2                              c = 2  lobe L: present 491, density 0.165822, inferable 64/64, mirrors 3, smallest endpoint keep Tm9 3
    c = 2                              c = 2  lobe R: present 525, density 0.177305, inferable 64/64, mirrors 3, smallest endpoint keep T5a 4
  w_min = 3: c = 1 has rank 1050 of 5922 pooled outside values (values >= 1)
    c* (pooled collapse, registered)   c = 1.15729  lobe L: present 498, density 0.168186, inferable 64/64, mirrors 3, smallest endpoint keep T5a 3
    c* (pooled collapse, registered)   c = 1.15729  lobe R: present 524, density 0.176967, inferable 64/64, mirrors 3, smallest endpoint keep T4a 4
    c* (restrict-only collapse)        c = 1.28713  lobe L: present 482, density 0.162783, inferable 64/64, mirrors 3, smallest endpoint keep T5a 3
    c* (restrict-only collapse)        c = 1.28713  lobe R: present 512, density 0.172915, inferable 64/64, mirrors 3, smallest endpoint keep T5a 3
    c* (b', full-grid density)         c = 2.83258  lobe L: present 395, density 0.133401, inferable 56/64, mirrors 1, smallest endpoint keep Tm9 1
    c* (b', full-grid density)         c = 2.83258  lobe R: present 419, density 0.141506, inferable 64/64, mirrors 1, smallest endpoint keep T4c 3
    c*_L (left lobe alone)             c = 1.04955  lobe L: present 511, density 0.172577, inferable 64/64, mirrors 3, smallest endpoint keep Tm9 3
    c*_L (left lobe alone)             c = 1.04955  lobe R: present 529, density 0.178656, inferable 64/64, mirrors 3, smallest endpoint keep T4a 4
    c*_R (right lobe alone)            c = 1.29892  lobe L: present 480, density 0.162107, inferable 64/64, mirrors 3, smallest endpoint keep T5a 3
    c*_R (right lobe alone)            c = 1.29892  lobe R: present 511, density 0.172577, inferable 64/64, mirrors 3, smallest endpoint keep T5a 3
    c = 0.5                            c = 0.5  lobe L: present 585, density 0.197568, inferable 64/64, mirrors 3, smallest endpoint keep T5a 4
    c = 0.5                            c = 0.5  lobe R: present 609, density 0.205674, inferable 64/64, mirrors 3, smallest endpoint keep T5a 4
    c = 1                              c = 1  lobe L: present 518, density 0.174941, inferable 64/64, mirrors 3, smallest endpoint keep Tm9 3
    c = 1                              c = 1  lobe R: present 532, density 0.179669, inferable 64/64, mirrors 3, smallest endpoint keep T4a 4
    c = 2                              c = 2  lobe L: present 423, density 0.142857, inferable 64/64, mirrors 2, smallest endpoint keep Tm9 2
    c = 2                              c = 2  lobe R: present 456, density 0.154002, inferable 64/64, mirrors 2, smallest endpoint keep T5a 3

peak memory 1261 MiB; runtime 7.3 s
written to C:\Users\mikha\Documents\dpc-research\connectome-seed-data\Janelia\derived\male_cns_v1_20260926T084555Z_e0a3cd744c39:
  male_cns_L_outside.csv: sha256 16c5752a241b2e61d4caeaa23bc4b9b9385011c2bfa6a2db504195199bfe9fb0, 15602 bytes
  male_cns_R_outside.csv: sha256 27a9079b656d1aeb1943702e173d2fa3009f7d8257a78f9e8b5c0f3712b4cf36, 16789 bytes
  pair_stats_outside.csv: sha256 dd71e686c50c127fa9b3bf9f05f957adbd1340d579c839361d16c6c0f0db421f, 263279 bytes
  male_cns_L_blockA.sealed.csv: sha256 eb611f6805484c4f54c22f072a2ca74219a97b3265c6bfb8a4639e45108e8b8e
  male_cns_R_blockA.sealed.csv: sha256 c53a44670b784f7af1c8c3973ba440961b24bff08b039a0cf4c73bd32414da84
  bank.meta.json: sha256 5ff4af9df5b6ca8e6bfb8282bb27a3b00697a4123b1885118a6d11057ab32d8b
```
