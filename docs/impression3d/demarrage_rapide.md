# Démarrage rapide avec les imprimantes 3D
## I. Téléchargement du modèle 3D

Pour commencer, vous aurez besoin d'un modèle 3D.  
Vous pouvez télécharger ce fichier: [Flexagon.stl](stl/flexagon.stl)  
Ou sur l'un des sites de partage de modèles 3D: [Où trouver des modèles 3D ?](ou_trouver_des_models_3d.md) 
 
---
 
## II. Installation et configuration de Bambu Studio

#### 1. Télécharger et installer <a href="https://bambulab.com/download" target="_blank" rel="noopener noreferrer"> Bambu Studio </a>
À la première ouverture de Bambu Studio, vous serez invité à sélectionner différents paramètres.
Laissez les paramètres par défaut et cliquez sur suivant jusqu'à arriver sur l'interface ci-dessous.
 
   <!--#### 2. Sélectionner de la région

   ![Sélection de la région](images/bambu/region.jpeg)
   
   ---
   

   #### 3.Sélection des l'imprimantes

   Cliquez sur **Tout effacer** puis sélectionner l'imprimante **X1 Carbon**.

   ![](images/bambu/imprimantes.jpeg)
   
   ---
   

   #### 4.Sélection du filament

   Les filaments les plus courants sont déjà présélectionnés cliquer sur suivant.

   ![](images/bambu/filaments.jpeg)
   
   ---
   

   #### 5. Ne pas installer le plugin réseau Bambu

   Décocher l'installation du plugin réseau et cliquer sur terminer. 

   ![](images/bambu/reseau.jpeg)
   
   ---

   ## Préparation de votre impression  -->

#### 2. Créer un nouveau projet

![](images/bambu/new_project.jpeg)

---

#### 3. Sélectionner la bonne imprimante 3D

Cliquer sur l'icône de l'imprimante 3D et sélectionner l'imprimante **X1 Carbon**.  

![](images/bambu/select_X1C.jpeg)

---
 
#### 4. Ajouter le modèle précédemment téléchargé 
Si ce n'est pas fait : [Téléchargement du modèle 3D](#i-telechargement-du-modele-3d)

Dans la barre d'outils supérieure, cliquez sur l'icône **ajouter** pour importer le modèle 3D.  
Vous pouvez également faire un glisser-déposer.  
Les fichiers pris en charge sont .3mf .stl .stp .step .amf .obj.   

![](images/bambu/insertion.jpeg)

---
 
#### 5. Positionner le modèle sur le plateau

Le modèle n'est pas forcément bien orienté sur le plateau.  
**Cliquer sur la fonction orientation automatique.**  
Il calcule l'orientation qui semble la plus pertinente.  
Si besoin, d'autres outils sont disponibles pour modifier manuellement, la position, l'échelle ou l'orientation du modèle.  


![](images/bambu/position.jpeg)

---

#### 6. Paramétrage de l'impression

Vérifiez que le filament (matière) est bien du **PLA**.  
Sélectionnez le profil de paramétrage **0.28mm Extra Draft**.

![](images/bambu/parametrage.jpeg)

Cliquez sur **Supports** et cochez la case **Activer les supports**.  
Puis cliquez sur **Trancher le plateau**.

![](images/bambu/supports.jpeg)

---

#### 7. Aperçu du tranchage
Le slicer vient de calculer les trajectoires d'impression, le temps d'impression et la quantité de filament nécessaire.  
Vous devriez avoir à peu près le même temps d'impression et quantité de matières que ci-dessous.  

![](images/bambu/apercu.jpeg)

---

#### 8. Exporter le fichier tranché (.3mf)

Cliquez sur la flèche et sélectionnez **Exporter le fichier tranché du plateau**.    
Puis cliquez sur le bouton **Exporter le fichier tranché du plateau**.  
Enregistrez le fichier .3mf sur votre ordinateur.

![](images/bambu/export.jpeg)

---

## III. 3D Printer OS

L'envoi du fichier à l'imprimante 3D se fait via le serveur 3D Printer OS.

### 1. Création du compte

Créer votre compte sur le site <a href="https://cloud.3dprinteros.com" target="_blank" rel="noopener noreferrer"> 3D Printer OS </a>.  
Utiliser votre adresse mail étudiante. 

### 2. Ajouter les imprimantes (WorkGroup)

Dans 3D Printer OS, cliquez sur **Printers** puis sur ![](images/3dprinteros/points.jpeg){ align=center width="30" class="off-glb"} et sur **Add workgroup Printers**.  
Demandez le code d'accès au responsable.

![](images/3dprinteros/workgroup.jpeg)

---

### 3. Ajout du fichier d'impression à 3D Printer OS

Dans l'onglet **Projects**, cliquez sur **Add files**.  
Sélectionnez le fichier .3mf, précédemment exporté de Bambu Studio.    

![](images/3dprinteros/add-files.jpeg)

---

### 4. Lancement de l'impression

Après avoir chargé le fichier, cliquez sur **Print**.  

![](images/3dprinteros/print.jpeg)


Sélectionnez l'imprimante 3D qui vous convient.  
Puis cliquez sur **Queue**.

![](images/3dprinteros/select-printer.jpeg) 

Sélectionnez la matière et la couleur à utiliser.
Puis cliquez sur **Queue**.

![](images/3dprinteros/queue.jpeg)


---

## IV. Préparation de l'imprimante 3D

Vérifiez sur l'imprimante 3D :

 - [x] Que le plateau d'impression est vide et sans résidu
 - [x] Que le plateau soit bien positionné  
 - [x] Que rien ne gêne les axes  
 - [x] Que la quantité de filaments est suffisante pour votre impression,  
 *voir l'onglet aperçu de Bambu Studio* 


<font size="6"> **:warning: Prévenez un responsable pour qu'il puisse valider l'impression et l'envoyer en production. :warning:** </font>

:warning: **Restez impérativement là pour vérifier les premières couches d'impression.** :warning:  
C'est souvent à ce moment que l'on détecte les problèmes d'impression.
 ---

## V. Récupération de votre impression 3D

Une fois l'impression terminée :  
Ouvrez la porte et décollez les traits de calibration sur le devant du plateau.  
Puis décollez vos pièces.  
Si la pièce a du mal à se décoller, demandez l'aide d'un responsable.  

Si vous voulez en savoir plus sur l'impression 3D --> [Les bases de l'impression 3D](les-bases-de-limpression-3d.md)