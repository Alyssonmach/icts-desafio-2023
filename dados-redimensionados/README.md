O dataset original foi obtido através do Google Drive, disponibilizado pelos criadores no GitHub, na qual o mesmo pode ser obtidos [clicando aqui](https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1Yz59yXCiPKS0_X4K3x9mW22NLnxjvrr0). Esse dataset foi adicionada a pasta ```dataset-original```. 

Em seguida, o script ```scripts/resize_image_and_annotation_final.py``` redimensiona as imagens e ajusta seus polígonos para 640x360. Execute-o a partir da raiz do repositório:

```
python scripts/resize_image_and_annotation_final.py -t dataset-original/ -o dados-redimensionados/
```

O script grava cada imagem JPG junto de seu JSON correspondente e define ```imageData``` como nulo para evitar manter os bytes da imagem original.
