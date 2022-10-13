// Tablolar Genel Özellikleri
$.extend($.fn.dataTable.defaults, {
  dom: "<'row'<'col-md-12'tr>>" + "<'row'<'col-md-4'l><'col-md-4'i><'col-md-4'p>>",
  "bDestroy": true,
  responsive: true,
  "pageLength": 25,
  "info": false,
  "language": {
    "paginate": {
      "next": "Sonraki Sayfa",
      "previous": "Önceki Sayfa"
    },
    "lengthMenu": "_MENU_ Kayıt",
    "zeroRecords":"Eşleşen kayıt bulunamadı",
  }
});

// Malzeme Tablosu
$(function () {
  $("#hammaddeler").DataTable({
    columnDefs: [
      { width: "2%", targets: 0 },
      { width: "20%", targets: 1 },
      { width: "8%", targets: 2 },
      { width: "10%", targets: 3 },
      { width: "12%", targets: 4 },
      { width: "16%", targets: 5 },
      { width: "14%", targets: 6 },
      { width: "15%", targets: 7 },
      { width: "10%", targets: 8 },
    ],
  });
  $("#hammadde_ara").on("input", function (e) {
    e.preventDefault();
    $("#hammaddeler").DataTable().search($(this).val()).draw();
  });
});


$(function () {
  $("#musteriler").DataTable({
    columnDefs: [
      { width: "1%", targets: 0 },
      { width: "8%", targets: 1 },
      { width: "8%", targets: 2 },
      { width: "4%", targets: 3 },
      { width: "20%", targets: 4 },
      { width: "5%", targets: 5 },
      { width: "8%", targets: 6 },
      { width: "2%", targets: 7 },
    ],
  });

  $("#musteri_ara").on("input", function (e) {
    e.preventDefault();
    $("#musteriler").DataTable().search($(this).val()).draw();
  });
});

$(function () {
  $("#siparisler").DataTable({

    columnDefs: [
      { width: "1%", targets: 0 },
      { width: "2%", targets: 1 },
      { width: "12%", targets: 2 },
      { width: "20%", targets: 3 },
      { width: "10%", targets: 4 },
      { width: "12%", targets: 5 },
      { width: "12%", targets: 6 },
      { width: "5%", targets: 7 },
      { width: "5%", targets: 8 },
      { width: "5%", targets: 9 },
      { width: "5%", targets: 10 },
      { width: "4%", targets: 11 },
      { width: "6%", targets: 12 },
    ],
  });

  $("#siparis_ara").on("input", function (e) {
    e.preventDefault();
    $("#siparisler").DataTable().search($(this).val()).draw();
  });
});