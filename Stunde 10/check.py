import sys
sys.path.insert(0, 'Z:/Codes/Unterricht/Schuster/Stunde 9')

import gebaeude, ressourcen, forschung

# Check GEBAEUDE_TYPEN
print('=== GEBAEUDE_TYPEN ===')
for i, g in enumerate(gebaeude.GEBAEUDE_TYPEN):
    print('  [' + str(i) + '] name=' + str(g['name']) + '  kuerzel=' + str(g['kuerzel']) + '  farbe=' + str(g['farbe']))

# Check GEBAEUDE_WIRTSCHAFT
print('\n=== GEBAEUDE_WIRTSCHAFT ===')
for i, w in enumerate(ressourcen.GEBAEUDE_WIRTSCHAFT):
    print('  [' + str(i) + '] ' + str(w))

# Check _gebaeude_name_fuer_index
print('\n=== _gebaeude_name_fuer_index ===')
for i in range(9):
    print('  [' + str(i) + '] = ' + str(ressourcen._gebaeude_name_fuer_index(i)))

# Check TECHNOLOGIEN
print('\n=== TECHNOLOGIEN ===')
for i, t in enumerate(forschung.TECHNOLOGIEN):
    print('  [' + str(i) + '] ' + str(t))
