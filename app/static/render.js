$(document).ready(function() {
    $('#deaths_by_age').DataTable( {
        "paging":   false,
        "searching": false,
        "info": false,
    });
    $('#general_stats').DataTable( {
        "paging":   false,
        "searching": false,
        "info": false,
        "ordering": false
    });
} );