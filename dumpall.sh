#!/bin/sh
echo "Elaboraciones"
python elbullidump.py --path data/1994-1997/CD1/elaboraciones/ > elaboraciones_1997.cd1.csv
python elbullidump.py --path data/1994-1997/CD2/elaboraciones/ > elaboraciones_1997.cd2.csv
python elbullidump.py --path data/1994-1997/CD3/ > elaboraciones_1997.cd3.csv
python elbullidump.py --path data/2003-2004/elaboracions/ > elaboraciones_2004.csv
python elbullidump.py --path data/2005/elaboracions/ > elaboraciones_2005.csv

echo "Estilos"
python elbullidump.py --path data/1994-1997/CD1/estilos/ > estilos_1997.cd1.csv
python elbullidump.py --path data/1994-1997/CD2/estilos/ > estilos_1997.cd2.csv
python elbullidump.py --path data/2003-2004/estils/ > estilos_2004.csv
python elbullidump.py --path data/2005/estils_i_caracteristiques/ > estilos_2005.csv

echo "Recetas"
python elbullidump.py --path data/1994-1997/CD1/recetas/ > recetas_1997.cd1.csv
python elbullidump.py --path data/1994-1997/CD2/recetas/ > recetas_1997.cd2.csv
python elbullidump.py --path data/2003-2004/receptes > recetas_2004.csv
python elbullidump.py --path data/2005/receptes/ > recetas_2005.csv

echo "Técnicas"
python elbullidump.py --path data/2005/tecniques_i_conceptes/ > tecnicas_2005.csv

