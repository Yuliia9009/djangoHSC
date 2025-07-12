document.addEventListener('DOMContentLoaded', function () {
    const regionSelect = document.getElementById('id_region');
    const tscSelect = document.getElementById('id_selected_tsc');

    if (!regionSelect || !tscSelect) return;

    regionSelect.addEventListener('change', function () {
        const regionId = this.value;
        fetch(`/autonumbers/ajax/load-tscs/?region=${regionId}`)
            .then(response => response.json())
            .then(data => {
                tscSelect.innerHTML = '<option value=""></option>';
                data.forEach(tsc => {
                    const option = document.createElement('option');
                    option.value = tsc.id;
                    option.textContent = tsc.name;
                    tscSelect.appendChild(option);
                });
            });
    });
});