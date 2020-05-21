$(document).ready(function() {
    console.log("monitor-status.js  ready!");

    MonitorStatus.start();
});

var MonitorStatus = {

    start: () => {
        console.log("MonitorStatus.start");
        MonitorStatus.updateStatuses();
    },

    updateStatuses: () => {
        console.log("MonitorStatus.updateStatuses");
        $('.status').each(function(i, obj) {

            if (obj.innerHTML == 'New') {
                obj.style.backgroundColor = "red";
                MonitorStatus.updateStatus(obj);

            } else if (obj.innerHTML == 'Processing') {
                obj.style.backgroundColor = "orange";
                MonitorStatus.updateStatus(obj);

            } else {
                obj.style.backgroundColor = "lime";
            }
        });

        setTimeout(MonitorStatus.updateStatuses, 5000);
    },

    updateStatus: (obj) => {
        console.log("MonitorStatus.updateStatus");
        console.log(obj);

        const pk = obj.id.replace("_status", "");

        $.getJSON(`/runs/${pk}/status/`)
        .done((data) => {
            console.log(data);
            obj.innerHTML = data.status_description

            if (data.status === 'C') {
                $('download-results').removeClass('d-none');
                $('view-render').removeClass('d-none');

                obj.style.backgroundColor = "lime";

            } else if (data.status === 'P') {
                obj.style.backgroundColor = "orange";
            }
        });

    }

};