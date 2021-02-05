(function() {
	$("span.fa").on("click", function() {
		var $span = $(this),
			$parentTr = $span.closest("tr");

		//remove
		if ($span.hasClass("fa-rotate-90")) {
			$span.removeClass("fa-rotate-90");
			$parentTr
				
				.next()
				.children("td")
				.animate({ padding: 0 })
				.wrapInner("<div />")
				.children()
				.slideUp(function() {
					var $tr = $(this).closest("tr");

					// $tr
					// 	.prev("tr")
					// 	.find(".active")
					// 	.removeClass("active");
					$tr.remove();
				$parentTr.removeClass("tr-selected");
				});

			return;
		}

		//add
		$span.addClass("fa-rotate-90");
		if ($parentTr.next().hasClass("tr-detail")) return;
		$parentTr.addClass("tr-selected");
		// 	.eq(1)
		// 	.addClass("active");
		$("#tr-detail")
			.clone()
			.removeClass("hidden")
			.insertAfter($parentTr)
			.children("td")
			.animate()
			.wrapInner("<div style='display:none'/>")
			.children()
			.slideDown();
	});
	
// 	$("i.fa").on("click", function() {
// 		$(this).closest("tr").next().removeClass("hidden").find("div.collapse").collapse("toggle");
// 	});
	
// 	$("div.collapse").on("hidden.bs.collapse", function(){
// 		$(this).closest("tr").children("td").css("padding","0")
// 								$(this).closest("tr").addClass("hidden")
// 								});
})();