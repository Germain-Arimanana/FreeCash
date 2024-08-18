import streamlit as st

def about():
    st.markdown(
                """
                 # <span style="color:#2E8B57;">Free Cash</span>
          
              ## <span style="color:#4682B4;">Description</span>
          
              Free Cash est une application de gestion financière interactive développée avec Streamlit, conçue pour simplifier la gestion de vos finances personnelles ou professionnelles. Elle offre une interface conviviale et intuitive, avec une série de fonctionnalités puissantes pour vous aider à organiser, analyser et présenter vos données financières. 
          
              ## <span style="color:#4682B4;">Fonctionnalités</span>
          
              ### <span style="color:#B22222;">1. SQLite3 - Gestion de la Base de Données</span>
              <span style="background-color:#FFFFE0;">Free Cash utilise SQLite3 comme moteur de base de données pour stocker toutes vos informations financières de manière sécurisée et efficace.</span> Grâce à SQLite3, vos données sont stockées localement, ce qui permet une gestion facile et un accès rapide aux informations sans besoin d'une connexion internet.
          
              ### <span style="color:#B22222;">2. Créer des Tables</span>
              L'application permet de créer des tables personnalisées pour organiser vos données financières. Chaque table peut représenter une catégorie spécifique, comme des revenus, des dépenses, ou des projets particuliers. Vous pouvez définir les colonnes de chaque table selon vos besoins, par exemple, <span style="color:#2E8B57;">Date, Description, Revenu, et Dépenses.</span>
          
              ### <span style="color:#B22222;">3. Fusionner les Tables</span>
              <span style="background-color:#FFFFE0;">Pour faciliter l'analyse de vos données, Free Cash vous permet de fusionner plusieurs tables en une seule.</span> Cette fonctionnalité est particulièrement utile si vous souhaitez consolider les informations provenant de différentes sources ou périodes pour avoir une vue d'ensemble de votre situation financière.
          
              ### <span style="color:#B22222;">4. Supprimer des Tables</span>
              Lorsque certaines tables ne sont plus nécessaires, vous pouvez les supprimer directement depuis l'application. Cette fonctionnalité vous aide à maintenir une base de données propre et bien organisée, sans données obsolètes.
          
              ### <span style="color:#B22222;">5. Exporter en PDF</span>
              Free Cash offre la possibilité d'exporter vos données sous forme de fichiers PDF. Que vous ayez besoin de partager vos rapports financiers ou simplement de les conserver pour des références futures, cette fonctionnalité assure que vos données sont présentées de manière professionnelle.
          
              ### <span style="color:#B22222;">6. Streamlit Chart</span>
              Visualisez vos données financières à l'aide de graphiques interactifs intégrés à l'application. Free Cash utilise les outils de visualisation de Streamlit pour créer des graphiques qui vous aident à mieux comprendre les tendances de vos finances, qu'il s'agisse de revenus, de dépenses ou d'autres indicateurs clés.
          
              ### <span style="color:#B22222;">7. Somme Automatique</span>
              <span style="background-color:#FFFFE0;">L'application calcule automatiquement les totaux de vos revenus et de vos dépenses pour chaque table.</span> Cela vous permet de suivre facilement vos finances sans avoir à faire les calculs manuellement. Vous pouvez également voir la différence entre vos revenus et vos dépenses pour évaluer votre solde global.
          
              ---
          
              ## <span style="color:#4682B4;">Open Source 🇲🇬🇲🇬</span>
          
              Free Cash est un projet open source, ce qui signifie que le code source est librement accessible à tous. Vous pouvez consulter, modifier, et améliorer le code selon vos besoins spécifiques. Nous encourageons la contribution de la communauté pour faire évoluer et enrichir l'application.
          
          
              """,unsafe_allow_html=True,)
