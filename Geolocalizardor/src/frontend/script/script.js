document.addEventListener("DOMContentLoaded", function() {
    var map = L.map("map").setView([-7.224661443928583, -35.88475675543521], 13);
    var marker;

    L.tileLayer('https://www.openstreetmap.org/export#map=4/-16.47/-45.92', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    document.getElementById('buscarCepBtn').addEventListener('click', function() {
        var cep = document.getElementById('cep').value;
        if (cep.trim() !== '') {
            buscarCoordenadasPorCEP(cep, function(coordenadas) {
                if (coordenadas) {
                    if (marker) {
                        map.removeLayer(marker); // Remove o marcador anterior, se existir
                    }
                    map.setView(coordenadas, 15); // Definir um zoom maior ao adicionar o marcador
                    marker = L.marker(coordenadas).addTo(map).bindPopup("Localização encontrada!");
                } else {
                    alert('CEP não encontrado ou serviço indisponível.');
                }
            });
        } else {
            alert('Por favor, insira um CEP válido.');
        }
    });

    function buscarCoordenadasPorCEP(cep, callback) {
        var url = 'https://viacep.com.br/ws/' + cep + '/json/';
        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (!data.erro) {
                    var endereco = data.logradouro + ', ' + data.localidade + ' - ' + data.uf;
                    buscarCoordenadasPorEndereco(endereco, callback);
                } else {
                    callback(null);
                }
            })
            .catch(error => {
                console.error('Erro ao buscar informações do CEP:', error);
                callback(null);
            });
    }

    function buscarCoordenadasPorEndereco(endereco, callback) {
        var url = 'https://nominatim.openstreetmap.org/search?format=json&q=' + encodeURIComponent(endereco);
        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    var coordenadas = [parseFloat(data[0].lat), parseFloat(data[0].lon)];
                    callback(coordenadas);
                } else {
                    callback(null);
                }
            })
            .catch(error => {
                console.error('Erro ao buscar coordenadas do endereço:', error);
                callback(null);
            });
    }
});