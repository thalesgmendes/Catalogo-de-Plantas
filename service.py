import requests

def get_plant_info(api_key, plant_name):
    # Endpoint para buscar plantas
    search_url = 'https://perenual.com/api/species-list'
    search_params = {
        'key': api_key,
        'q': plant_name
    }

    # Fazendo a requisição para buscar a planta
    search_response = requests.get(search_url, params=search_params)

    if search_response.status_code == 200:
        search_data = search_response.json()
        if search_data['data']:
            # Pegando o ID da primeira planta encontrada
            plant_id = search_data['data'][0]['id']

            # Endpoint para detalhes da planta
            details_url = f'https://perenual.com/api/species/details/{plant_id}'
            details_params = {
                'key': api_key
            }

            # Fazendo a requisição para obter detalhes da planta
            details_response = requests.get(details_url, params=details_params)

            if details_response.status_code == 200:
                details_data = details_response.json()

                # Extraindo informações relevantes
                plant_info = {
                    'name': details_data.get('common_name', 'N/A'),
                    'scientific_name': details_data.get('scientific_name', 'N/A'),
                    'watering': details_data.get('watering', 'N/A'),
                    'sunlight': details_data.get('sunlight', 'N/A'),
                    'care_level': details_data.get('care_level', 'N/A'),
                    'soil_type': details_data.get('soil', 'N/A'),  # Adicionando tipo de solo
                    'image_url': details_data.get('default_image', {}).get('original_url', 'N/A')
                }

                return plant_info
            else:
                print(f"Erro ao obter detalhes da planta: {details_response.status_code}")
                return None
        else:
            print("Planta não encontrada.")
            return None
    else:
        print(f"Erro na busca da planta: {search_response.status_code}")
        return None

def main():
    api_key = 'sk-gnfJ67c8fd0b098238981'
    plant_name = input("Digite o nome da planta: ")

    plant_info = get_plant_info(api_key, plant_name)

    if plant_info:
        print("\nInformações da Planta:")
        print(f"Nome: {plant_info['name']}")
        print(f"Nome Científico: {plant_info['scientific_name']}")
        print(f"Requisitos de Água: {plant_info['watering']}")
        print(f"Requisitos de Luz Solar: {plant_info['sunlight']}")
        print(f"Nível de Cuidado: {plant_info['care_level']}")
        print(f"Tipo de Solo Ideal: {plant_info['soil_type']}")  # Exibindo tipo de solo
        print(f"URL da Imagem: {plant_info['image_url']}")

if __name__ == "__main__":
    main()