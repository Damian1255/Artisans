$(function () {
    // ajax call for getting data 
    $.ajax({
        url: "http://127.0.0.1:5000/admin/data",
        type: "POST",
        dataType: "json",
        success: function (data) {
            var result = data

            // revenue chart
            $("#total-revenue").text("$" + result.result_bydate.sales.reduce((a, b) => a + b, 0))

            // revenue status since previous day
            prev = result.result_bydate.sales[result.result_bydate.sales.length - 2]
            current = result.result_bydate.sales[result.result_bydate.sales.length - 1]
            
            if (prev == 0) {
                html = `<p class="mb-0 font-13 text-success"><i class="fa bx bxs-up-arrow text-success"></i> 100% Since Previous Day</p>`
            } else if (prev > current) {
                html = `<p class="mb-0 font-13 text-danger"><i class="fa bx bxs-down-arrow text-danger"></i> ${Math.round((prev - current) / prev * 100)}% Since Previous Day</p>`
            } else {
                html = `<p class="mb-0 font-13 text-success"><i class="fa bx bxs-up-arrow text-success"></i> ${Math.round((current - prev) / prev * 100)}% Since Previous Day</p>`
            }
            $("#rev-status").append(html)

            "use strict";
            var e = {
                series: [{ name: "Revenue", data: result.result_bydate.sales }],
                chart: { type: "line", height: 65, toolbar: { show: !0, tools: { download: true } }, zoom: { enabled: !1 }, dropShadow: { enabled: !0, top: 3, left: 14, blur: 4, opacity: 0.12, color: "#17a00e" }, sparkline: { enabled: !0 } },
                markers: { size: 0, colors: ["#17a00e"], strokeColors: "#fff", strokeWidth: 2, hover: { size: 7 } },
                dataLabels: { enabled: !1 },
                stroke: { show: !0, width: 3, curve: "smooth" },
                colors: ["#17a00e"],
                xaxis: { type: 'date', categories: result.result_bydate.date },
                fill: { opacity: 1 },
                tooltip: {
                    theme: "dark",
                    fixed: { enabled: !1 },
                    x: { show: !0 },
                    y: {
                        title: {
                            formatter: function (e) {
                                return "Revenue ($)";
                            },
                        },
                        formatter: function (e) {
                            return "$" + e;
                        },
                    },
                    marker: { show: !1 },
                },
            };
            new ApexCharts(document.querySelector("#chart1"), e).render();

            // quantity chart
            $("#total-quantity").text(result.result_bydate.quantity.reduce((a, b) => a + b, 0))

            // quantity status since previous day
            prev = result.result_bydate.quantity[result.result_bydate.quantity.length - 2]
            current = result.result_bydate.quantity[result.result_bydate.quantity.length - 1]

            if (prev == 0) {
                html = `<p class="mb-0 font-13 text-success"><i class="fa bx bxs-up-arrow text-success"></i> 100% Since Previous Day</p>`
            } else if (prev > current) {
                html = `<p class="mb-0 font-13 text-danger"><i class="fa bx bxs-down-arrow text-danger"></i> ${Math.round((prev - current) / prev * 100)}% Since Previous Day</p>`
            } else {
                html = `<p class="mb-0 font-13 text-success"><i class="fa bx bxs-up-arrow text-success"></i> ${Math.round((current - prev) / prev * 100)}% Since Previous Day</p>`
            }

            $("#qty-status").append(html)

            e = {
                series: [{ name: "Customers", data: result.result_bydate.quantity }],
                chart: { type: "line", height: 65, toolbar: { show: !0, tools: { download: true } }, zoom: { enabled: !1 }, dropShadow: { enabled: !0, top: 3, left: 14, blur: 4, opacity: 0.12, color: "#ffc107" }, sparkline: { enabled: !0 } },
                markers: { size: 0, colors: ["#ffc107"], strokeColors: "#fff", strokeWidth: 2, hover: { size: 7 } },
                dataLabels: { enabled: !1 },
                stroke: { show: !0, width: 3, curve: "smooth" },
                colors: ["#ffc107"],
                xaxis: { categories: result.result_bydate.date },
                fill: { opacity: 1 },
                tooltip: {
                    theme: "dark",
                    fixed: { enabled: !1 },
                    x: { show: !0 },
                    y: {
                        title: {
                            formatter: function (e) {
                                return "Sold";
                            },
                        },
                    },
                    marker: { show: !1 },
                },
            };
            new ApexCharts(document.querySelector("#chart2"), e).render();

            // profit chart
            $("#total-profit").text("$" + result.result_bydate.profit.reduce((a, b) => a + b, 0))

            // profit status since previous day
            prev = result.result_bydate.profit[result.result_bydate.profit.length - 2]
            current = result.result_bydate.profit[result.result_bydate.profit.length - 1]

            if (prev == 0) {
                html = `<p class="mb-0 font-13 text-success"><i class="fa bx bxs-up-arrow text-success"></i> 100% Since Previous Day</p>`
            } else if (prev > current) {
                html = `<p class="mb-0 font-13 text-danger"><i class="fa bx bxs-down-arrow text-danger"></i> ${Math.round((prev - current) / prev * 100)}% Since Previous Day</p>`
            } else {
                html = `<p class="mb-0 font-13 text-success"><i class="fa bx bxs-up-arrow text-success"></i> ${Math.round((current - prev) / prev * 100)}% Since Previous Day</p>`
            }

            $("#profit-status").append(html)
            
            e = {
                series: [{ name: "Profit", data: result.result_bydate.profit }],
                chart: { type: "line", height: 65, toolbar: { show: !0, tools: { download: true } }, zoom: { enabled: !1 }, dropShadow: { enabled: !0, top: 3, left: 14, blur: 4, opacity: 0.12, color: "#f41127" }, sparkline: { enabled: !0 } },
                markers: { size: 0, colors: ["#f41127"], strokeColors: "#fff", strokeWidth: 2, hover: { size: 7 } },
                dataLabels: { enabled: !1 },
                stroke: { show: !0, width: 3, curve: "smooth" },
                colors: ["#f41127"],
                xaxis: { categories: result.result_bydate.date },
                fill: { opacity: 1 },
                tooltip: {
                    theme: "dark",
                    fixed: { enabled: !1 },
                    x: { show: !0 },
                    y: {
                        title: {
                            formatter: function (e) {
                                return "Profit ($)";
                            },
                        },
                        formatter: function (e) {
                            return "$" + e;
                        },
                    },
                    marker: { show: !1 },
                },
            };
            new ApexCharts(document.querySelector("#chart3"), e).render();
            
            // sales and profit chart
            $("#metric-rev").text("$" + result.result_bydate.sales.reduce((a, b) => a + b, 0))
            $("#metric-qty").text(result.result_bydate.quantity.reduce((a, b) => a + b, 0))
            $("#metric-profit").text("$" + result.result_bydate.profit.reduce((a, b) => a + b, 0))

            // profit status since previous day
            prev = result.result_bydate.profit[result.result_bydate.profit.length - 2]
            current = result.result_bydate.profit[result.result_bydate.profit.length - 1]

            if (prev > current) {
                html = `<p class="mb-0 font-13 text-danger"><i class="fa bx bxs-down-arrow text-danger"></i> $${Math.round(prev - current)} Since Previous Day</p>`
            } else {
                html = `<p class="mb-0 font-13 text-success"><i class="fa bx bxs-up-arrow text-success"></i> $${Math.round(current - prev)} Since Previous Day</p>`
            }

            $("#metric-status-profit").append(html)

            // sales status since previous day
            prev = result.result_bydate.sales[result.result_bydate.sales.length - 2]
            current = result.result_bydate.sales[result.result_bydate.sales.length - 1]

            if (prev > current) {
                html = `<p class="mb-0 font-13 text-danger"><i class="fa bx bxs-down-arrow text-danger"></i> $${Math.round(prev - current)} Since Previous Day</p>`
            } else {
                html = `<p class="mb-0 font-13 text-success"><i class="fa bx bxs-up-arrow text-success"></i> $${Math.round(current - prev)} Since Previous Day</p>`
            }

            $("#metric-status-rev").append(html)

            // quantity status since previous day
            prev = result.result_bydate.quantity[result.result_bydate.quantity.length - 2]
            current = result.result_bydate.quantity[result.result_bydate.quantity.length - 1]

            if (prev > current) {
                html = `<p class="mb-0 font-13 text-danger"><i class="fa bx bxs-down-arrow text-danger"></i> ${Math.round(prev - current)} Since Previous Day</p>`
            } else {
                html = `<p class="mb-0 font-13 text-success"><i class="fa bx bxs-up-arrow text-success"></i> ${Math.round(current - prev)} Since Previous Day</p>`
            }

            $("#metric-status-qty").append(html)

            e = {
                series: [
                    { name: "Total Sales", data: result.result_bydate.sales },
                    { name: "Profit", data: result.result_bydate.profit },
                ],
                chart: { foreColor: "#9ba7b2", type: "bar", height: 300, toolbar: { show: !0, tools: { download: true } } },
                plotOptions: { bar: { horizontal: !1, columnWidth: "55%", endingShape: "rounded" } },
                dataLabels: { enabled: !1 },
                stroke: { show: !0, width: 2, colors: ["transparent"] },
                colors: ["#0dcaf0", "#0d6efd"],
                xaxis: { categories: result.result_bydate.date },
                tool: { download: true },
                fill: { opacity: 1 },
                tooltip: {
                    y: {
                        formatter: function (e) {
                            return "$" + e;
                        },
                    },
                },
                yaxis: {
                    labels: {
                        formatter: function (value) {
                            return "$" + Math.round(value);
                        }
                    }
                }
            };
            new ApexCharts(document.querySelector("#chart4"), e).render();

            // sales and profit chart
            e = {
                series: [
                    {
                        name: "Total Sales",
                        data: result.result_bydate.sales
                    },
                    {
                        name: "Profit",
                        data: result.result_bydate.profit
                    }
                ],
                chart: {
                    height: 350,
                    type: 'line',
                    dropShadow: {
                        enabled: true,
                        color: '#000',
                        top: 18,
                        left: 7,
                        blur: 10,
                        opacity: 0.2
                    },
                    toolbar: { show: !0, tools: { download: true } } 
                },
                colors: ["#0dcaf0", "#0d6efd"],
                stroke: {
                    curve: 'smooth'
                },

                grid: {
                    borderColor: '#e7e7e7',
                    row: {
                        colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                        opacity: 0.5
                    },
                },
                markers: {
                    size: 1
                },
                xaxis: {
                    categories: result.result_bydate.date,
                },
                tooltip: {
                    y: {
                        formatter: function (e) {
                            return "$" + e;
                        },
                    },
                },
                yaxis: {
                    labels: {
                        formatter: function (value) {
                            return "$" + Math.round(value);
                        }
                    }
                }
            };
            new ApexCharts(document.querySelector("#chart5"), e).render();

            // sales by category chart
            colors = ["#17a00e", "#0d6efd", "#f41127", "#ffc107", "#0dcaf0"]

            $("#category-list").append(result.result_topcategory.category.map(function (category) {
                color = colors[result.result_topcategory.category.indexOf(category)]
                amount = result.result_topcategory.sales[result.result_topcategory.category.indexOf(category)]

                return `<li class="list-group-item d-flex justify-content-between align-items-center">${category}
                <span style="background-color:${color}" class="badge rounded-pill">$${amount}</span>`
            }))

            e = {
                series: result.result_topcategory.sales,
                chart: { height: 240, type: "donut", toolbar: { show: !0, tools: { download: true } } },
                legend: { position: "bottom", show: !1 },
                plotOptions: { pie: { donut: { size: "60%" } } },
                colors: colors,
                dataLabels: { enabled: !1 },
                labels: result.result_topcategory.category,
                responsive: [{ breakpoint: 480, options: { chart: { height: 200 }, legend: { position: "bottom" } } }],
                tooltip: {
                    y: {
                        formatter: function (e) {
                            return "$" + e;
                        },
                    },
                }
            };
            new ApexCharts(document.querySelector("#chart15"), e).render();

            // top selling products chart
            $("#product-list").append(result.result_topproduct.product.map(function (product) {
                product = result.result_topproduct.product[result.result_topproduct.product.indexOf(product)]
                amount = result.result_topproduct.sales[result.result_topproduct.product.indexOf(product)]
                quantity = result.result_topproduct.quantity[result.result_topproduct.product.indexOf(product)]
                id = result.result_topproduct.product_id[result.result_topproduct.product.indexOf(product)]

                return `
                <div class="row border mx-0 mb-3 py-2 radius-10 cursor-pointer">
                    <div class="col-sm-6">
                        <div class="d-flex align-items-center">
                            <div class="ms-2">
                                <h6 class="mb-1">${product}</h6>
                                <a href='/admin/products/${id}'>View Product</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-sm">
                        <h6 class="mb-1">$${amount}</h6>
                        <p class="mb-0">${quantity} Sales</p>
                    </div>
                    <div class="col-sm">
                        <div id="chart${id}"></div>
                    </div>
                    </div>
                </div>`
            }))

            // loop through each product and create a chart
            for (i in result.result_products) {
                date = result.result_products[i][0]
                quantity = result.result_products[i][1]
                e = {
                    series: [{ name: "Revenue", data: quantity }],
                    chart: { type: "area", height: 45, toolbar: { show: !0, tools: { download: true } }, zoom: { enabled: !1 }, dropShadow: { enabled: !1, top: 3, left: 14, blur: 4, opacity: 0.12, color: "#0d6efd" }, sparkline: { enabled: !0 } },
                    markers: { size: 0, colors: ["#0d6efd"], strokeColors: "#fff", strokeWidth: 2, hover: { size: 7 } },
                    dataLabels: { enabled: !1 },
                    stroke: { show: !0, width: 2, curve: "smooth" },
                    colors: ["#0d6efd"],
                    xaxis: { categories: date },
                    fill: { opacity: 1 },
                    tool: { download: true },
                    tooltip: {
                        theme: "dark",
                        fixed: { enabled: !1 },
                        x: { show: !0 },
                        y: {
                            title: {
                                formatter: function (e) {
                                    return "Quantity Sold";
                                },
                            },
                        },
                        marker: { show: !1 },
                    },
                };
                new ApexCharts(document.querySelector("#chart" + i), e).render();
            }
        }
    });

    $("#switch-bar").click(function () {
        $("#chart4").css("display", "block")
        $("#chart5").css("display", "none")
    });

    $("#switch-line").click(function () {
        $("#chart4").css("display", "none")
        $("#chart5").css("display", "block")
    });

});
