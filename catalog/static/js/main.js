$(document).ready(function () {
    $("#create_category").click(function () {
        if ($('#category_name').val() == '' || $("#category_description").val() == '') {
            return;
        }
        $.post("/category/create",
            {
                category_name: $("#category_name").val(),
                category_description: $("#category_description").val()
            },
            function (data, status) {
                var obj = JSON.parse(data);

                if (obj.status != "0") {
                    alert("Category already exists.");
                    return;
                }

                alert("Created : " + obj.category_name);
                $('#category_name').val('');
                $('#category_description').val('');
            });
    });
});