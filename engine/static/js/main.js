$(document).ready(function() {
    function get_product_details(pk){
        $.ajax({
            url: "/product/" + pk + "/",
            type: 'GET',
            success: function(product){
                $('#productView-img').attr("src", product.img_big);
                $('#productView-category').html(product.category);
                $('#productView-name').html(product.name);
                $('#productView-description').html(product.description);
                $('#productView-price').html(product.price);
                $('#productView-amount').html(product.amount);
                $('#productView').css("display", "block");
            }
        });
    }

    $(".product").click(function() {
        get_product_details(parseInt($(this).data("pk")));
    });

    $(".close").click(function() {
        $('#productView').css("display", "none");
    });
});
