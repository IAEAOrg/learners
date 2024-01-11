---
title: Modèle d'exercice
menuTitle: Modèle d'exercice
weight: 4
chapter: false
---

{{< toc >}}

---

## Exemple d'en-tête de section

### Exemple d'en-tête de sous-section

Dans cette page, vous trouverez un modèle pour tous les types de contenu autorisés dans Learners.

## Tables

### Formatage de base de l'en-tête

| Header1: Left | Header2: Center | Header3: Right |
|:-------| :-----: |-----: |
| lorem ipsum ... | lorem ipsum ... | lorem ipsum ... |

### Tableau avec images

| Image | Description |
|:---| :-----|
| ![alt text](image.PNG) | lorem ipsum ... |

### Options du tableau de présentation

| {{< layout-table ratio="50 50" striped="true" divider="true" padding="20px 40px 20px 0px" >}} |    |
| :--------------------------------- | :-------------- |
| ![alt text](image.PNG)             | lorem ipsum ... |
| ![alt text](image.PNG)             | lorem ipsum ... |

## Images et figures

### Pas de légende

![alt text](image2.PNG)

### Légende

![This is a Figure](image2.PNG#figure)

## Formulaires d'exercice

Le formulaire d'exercice enregistre les réponses des participants et permet de les soumettre. Chaque formulaire est une combinaison de plusieurs types d'entrées différentes.

{{% form name="Exercise Template" %}}

{{% input-group title="Example Input Group" extendable="true" min="0" %}}

{{< input-text
    label="Required input field with instructor information:"
    wide=true
    required=true
    placeholder="Please enter the answer"
    instructor="Here is the note for the instructor"
>}}

{{< input-text
    label="Optional input field without instructor information:"
    wide=true
    required=false
    placeholder="Please enter the answer"
>}}

{{< input-textarea
    label="Text area:"
    required=false
    placeholder="Please enter the answer"
>}} <!-- Same options of the input-text apply-->

{{< input-select label="Drop-down menu:" options="Option 1; Option 2; Option 3" >}} <!-- Same options of the input-text apply-->

{{< input-file label="File Uploader:" required=false wide=false >}}

{{< input-risk >}} <!-- Very specific type of input to calculate risk based on likelihood and impact -->

{{% /input-group %}}

## plugin draw.io

{{< input-group title="Incident Timeline" >}}

Utilisez le modèle présenté ci-dessous pour construire une chronologie de l'incident qui soit caractérisée par les IoC que vous avez identifiés. Pour ce faire, cliquez sur le bouton Editer dans DrawIO pour ouvrir un nouvel onglet de navigateur avec un diagramme préparé à l'avance qui peut être utilisé pour réaliser cet exercice. Lorsque vous avez terminé, collez l'URL du diagramme dans la boîte de soumission ci-dessous en choisissant Fichier, Publier, Lien..., Créer, puis en copiant l'URL générée.

{{< drawio data="?title=DrawIO_Example#RzZbBjpswEIafpQeOKxkMJDku7G572GqrRu22RxcPYNVgZJwN6dN3CCaEQJRGSqXlkNj%2FGOz5%2FrHBoXHRfNSsyj8rDtLxCG8c%2BuB4nkcWPv61yq5TXDcMOyXTglttENbiD1iRWHUjONSjgUYpaUQ1FhNVlpCYkca0VtvxsFTJ8awVy2AirBMmp%2Bqr4Ca3ahj4Q%2BATiCw3hwRXXaRg%2FWibSp0zrrZHEn10aKyVMl2raGKQLb4eTHff05noYWUaSvMvN5ivsWTxywtdie%2FfVPTj%2Beddemef8sbkxmb8CjJRBexB488zMF2Crj%2FYJMyuR2OgwXmj3BQSBRebtdHqN8RKKo1KqUocGaVCyhOJSZGV2E1w5YB69AbaCIR%2BbwOF4LydJtrmwsC6Ykk75xZrDDWtNiWHNilymLP3pl1FqkpjCyn0sW8zxCmgOYvOPRiCtQyYv9E7HGJvoEvrYV%2FG1Pa3Q00s%2BjH5cTn0IrN1mB2ePTiFDWvWFcZ5E%2BMmBs3BO3KL1VW3Y1LRtDhHTjke5UtCFtQCPdLT%2FTWxGyP3ASE%2BuQ1yPxwjp2SKfI74fwNOLwPHp%2BC5dK5ur0BPyJIRcg16QoIFuRH60H9n6P3L6HWuil%2Bb%2BjL6E9JAk%2BUcabK%2F5khHZBXcivTSfWekg8uk8TVWtU3MkkkJUmWaFYijAi1wEe15Po59GQKXzcHtYM%2FuGbMYCTyPX7Mtwgf36VZmrU5PJHdqluvNuBVe7xZ2hw%2BDfezoA4s%2B%2FgU%3D" >}}

{{% /input-group %}}

{{% /form %}}

{{< downloadPDF >}}  <!-- This allows the participant to download the page -->
{{< input-comment >}} <!-- This creates a feedback form for the participants -->
