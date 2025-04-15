import numpy as np
from tabulate import tabulate

#Constante RI
RI = {1: 0,2:0,3:0.58,4:0.9,5:1.12,6:1.24,7:1.32,8:1.41,9:1.45,10:1.49}
ACTION_LIST = ['o', 'n']

#Definir la class pour stocker les differents criteres et leur poids
class Criteria:
    def __init__(self, criterial_name : str):
        self.criteria_name = criterial_name
        self.criteria_weight = None

    def __str__(self):
        return self.criteria_name

    def update_weight(self, weight):
        self.criteria_weight = weight

    def __repr__(self):
        return self.criteria_name

class Alternative:
    def __init__(self, alternative_name : str):
        self.alternative_name = alternative_name
        self.caracteristics = dict()

    def __str__(self):
        return self.alternative_name

    def __repr__(self):
        return self.alternative_name

    def add_caracteristic(self, criteria : Criteria, info : float):
        
        if criteria.criteria_name not in self.caracteristics.keys():
            self.caracteristics[criteria.criteria_name] = {"criteria":criteria, "value":info}
        else: 
            print(f"L'alternative presente deja des données sur {criteria.criteria_name}")
            action = input("Voulez vous ecraser ces donnée ? [O/n]")
            action = action.lower()
            while action not in ACTION_LIST :
                print("Erreur de saisie...")
                action = input("Voulez vous ecraser ces donnée ? [O/n]")
                action = action.lower()
            if action == 'o':
                self.caracteristics[criteria.criteria_name] = {"criteria":criteria, "value":info}           

def print_matrix2(headers : list, indexs: list,matrix , col_marge=None, colmarge_name="" ,row_marge = None, rowmarge_name = ""):
    
    
    tabular_data = []
    for i, elt in enumerate(indexs):
        line = [elt]
        for j, _ in enumerate(headers):
            line.append(f"{matrix[i,j]:.4f}")
        
        if row_marge!=None:
            line.append(f"{row_marge[i]:.4f}")
        tabular_data.append(line)
    
    if row_marge!=None:
        headers.append(rowmarge_name)
        
    if col_marge !=None:
        line = [colmarge_name]
        for e in col_marge:
            line.append(f"{e:.4f}")
        tabular_data.append(line)
    
    print(tabulate(tabular_data=tabular_data, headers=headers, tablefmt="grid", stralign="center", numalign="center"))

#Fonction pour l'affichage des matrices
def print_matrix(criteria_list : list, matrix , col_marge=None, colmarge_name="" ,row_marge = None, rowmarge_name = ""):
    
    header = [""]
    for e in criteria_list:
        header.append(e.criteria_name)

    if row_marge!=None:
        header.append(rowmarge_name)
    
    tabular_data = []
    for i, e in enumerate(criteria_list):
        line = [e.criteria_name]
        for j, _ in enumerate(criteria_list):
            line.append(f"{matrix[i,j]:.4f}")
        
        if row_marge!=None:
            line.append(f"{row_marge[i]:.4f}")
        tabular_data.append(line)
    
    if col_marge !=None:
        line = [colmarge_name]
        for e in col_marge:
            line.append(f"{e:.4f}")
        tabular_data.append(line)
    
    print(tabulate(tabular_data=tabular_data, headers=header, tablefmt="grid", stralign="center", numalign="center"))


print("0- Criteres et preferences\n")


#Entrer nombre de criteres
print("0.1- Entrer les criteres :\n")
nb_criteria = input("Entrer le nombre de criteres : ")
stop = True
while stop:
    try :
        nb_criteria = int(nb_criteria)
        stop = False
    except :
        print("Valeur entrée n'est pas entiere...")
        nb_criteria = input("Entrer le nombre de criteres : ")

#Entrer la liste de critere
print("\nEntrer la liste de critere :")
critera_list =[]
for i in range(nb_criteria):
    critera_name = input(f"\t{i+1} :: Entrer le nom du {i+1}ieme critere : ")
    critera_list.append(Criteria(critera_name))

#Entrer les preferences 
#Pour chaque critere on donne les preferences par rapport aux autres et on rempli la matrice 
print("\n0.2- Entrer la matrice des preferences des criteres : \n")
criteria_matrix = np.eye(nb_criteria, dtype=float)
for i in range(nb_criteria-1):
    print(f"Ligne :: {i}")
    for j in range(i+1, nb_criteria):
        preference = input(f"\tPreference de {critera_list[i]} par rapport a {critera_list[j]} : ")
        stop = True
        while stop:
            try :
                preference = float(preference)
                stop = False
            except :
                print("Valeur entrée n'est pas reel...")
                preference = input(f"Preference de {critera_list[i]} par rapport a {critera_list[j]} : ")
                
        criteria_matrix[i,j] = preference
    print("\n")
for i in range(1, nb_criteria):
    for j in range(i):
        criteria_matrix[i, j] = 1/criteria_matrix[j, i]

#Creer une copy de la matrice pour les prochains calculs
pred_matrix = np.copy(criteria_matrix)
print("1- Matrice des preferences :\n")
print_matrix(criteria_list=critera_list, matrix=pred_matrix, col_marge=list(np.sum(pred_matrix, axis=0)), colmarge_name="Column Sum")

#Normaliser les preferences : La somme de chaque colonne egale a 1
criteria_colSum = np.sum(criteria_matrix, axis=0)
for i, val in enumerate(criteria_colSum):
    criteria_matrix[:,i] = criteria_matrix[:,i]/criteria_colSum[i]

print("\n2- Matrice des preferences normalisées :\n")
tmp = list(np.sum(criteria_matrix, axis=0))
print_matrix(critera_list, criteria_matrix, col_marge=tmp, colmarge_name="Column Sum")

#Calcul du poids de chaque critère et stockage dans les objets Criteria 
criteria_rowSum = np.sum(criteria_matrix, axis=1) 

print("\n3- Calcul des poids des criteres :")
print("\n3.1- Matrice des preferences avec les sommes de chaque ligne :\n")
print_matrix(critera_list, criteria_matrix, row_marge=list(criteria_rowSum), rowmarge_name="Row Sum")

criterial_weight = criteria_rowSum/nb_criteria
for i, weight in enumerate(criterial_weight):
    critera_list[i].update_weight(weight)

print("\n3.2- Matrice des preferences avec les poids des criteres :\n")
print_matrix(critera_list, criteria_matrix, row_marge=list(criterial_weight), rowmarge_name="Critera Weight")

#Calcul du criteria weight sum 
pred_dot_weight = pred_matrix*criterial_weight
criteria_weight_sum = np.sum(pred_dot_weight,axis=1)
print("\n3.3- Matrice des preferences avec les criteria weight sum :\n")
print_matrix(critera_list, criteria_matrix, row_marge=list(criteria_weight_sum), rowmarge_name="Critera Weight Sum")

#Calcul de lambda weight, lambda max, CI et CR
lambda_weight = criteria_weight_sum/criterial_weight
lambda_max = np.mean(lambda_weight) 
CI = (lambda_max - nb_criteria)/(nb_criteria -1)
CR = CI/RI[nb_criteria]
CR, RI[nb_criteria]

table = []
for i, e in enumerate(critera_list):
    table.append([e.criteria_name, f"{lambda_weight[i]:.4f}"])

print("\n5- Les Metriques :")
print("\n5.1- Valeur lambda de chaque critere :\n")
print(tabulate(tabular_data=table, headers=["Criteria", "Lambda"], tablefmt="grid", stralign="center", numalign="center"))

print("\n5.2- Autres metriques (Lambda max, CI, CR, RI) :\n")
table = [["Lambda Max", f"{lambda_max:.4}"], ["CI", f"{CI:.4f}"], ["CR",f"{CR:.4f}"], ["RI", f"{RI[nb_criteria]:.4f}"]]
print(tabulate(tabular_data=table, headers=["Metrique", "Valeur"], tablefmt="grid", stralign="center", numalign="center"))

if CR<0.10 :
    next_step = True
    print(f"La valeur CR = {CR:.4f} < 0.10 alors la prise de decision est consistante...")
else :
    next_step = False
    print(f"La valeur CR = {CR:.4f} >= 0.10 alors la prise de decision n'est pas consistante...")

if next_step:
    print("\n6- Alternatives : ")
    print("\n6.1- Entrer les alternatives :\n")
    nb_alternatives = input("Entrer le nombre d'alternatives : ")
    stop = True
    while stop:
        try :
            nb_alternatives = int(nb_alternatives)
            stop = False
        except :
            print("Valeur entrée n'est pas entiere...")
            nb_alternatives = input("Entrer le nombre d'alternatives : ")

    print("Entrer la liste d'alternatives : ")
    alternatives_list = []
    matrix_alternative = []
    for i in range(nb_alternatives):
        alternative_name = input(f"\n{i} :: Entrer la {i+1}ieme alternative : ")
        alternatives_list.append(Alternative(alternative_name))
        line = []
        for critera in critera_list:
            info = input(f"\tEntrer la valeur du critere {critera.criteria_name} pour {alternative_name} : ")
            stop = True
            while stop:
                try :
                    info = float(info)
                    stop=False
                except :
                    print("Erreur, la valeur entree doit etre un reel...")
                    info = input(f"\tEntrer la valeur du critere {critera.criteria_name} pour {alternative_name} : ")
                    
            alternatives_list[i].add_caracteristic(critera, info)
            line.append(info)
        matrix_alternative.append(line)
    matrix_alternative = np.array(matrix_alternative)
    matrix_choises = matrix_alternative*criterial_weight
    total_item_weight = np.sum(matrix_choises, axis=1)

    critera_list_ = [e.criteria_name for e in critera_list]
    alternatives_list_ = [e.alternative_name for e in alternatives_list]
    print("\n6.2- Caracteristiques des alternatives :\n")
    print_matrix2(critera_list_, alternatives_list_, matrix_alternative)

    print("\n6.3- Final results :\n")
    print_matrix2(critera_list_, alternatives_list_, matrix_choises, row_marge=list(total_item_weight), rowmarge_name="Total Item Weight")

    print(f"\nLa meilleure alternative est : {alternatives_list_[np.argmax(total_item_weight)]}")
    
    