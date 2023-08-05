$(function () {

  $.ajax({
    url: "http://127.0.0.1:5000/support/data",
    type: "POST",
    dataType: "json",
    success: function (data) {
      var result = data
      console.log(result)

      // chart 13
      var options = {
        chart: {
          height: 310,
          type: 'bar',
          toolbar: {
            show: false
          }
        },
        plotOptions: {
          bar: {
            columnWidth: '50%',
            endingShape: 'rounded',
            dataLabels: {
              position: 'top', // top, center, bottom
            },
          }
        },
        dataLabels: {
          enabled: true,
          formatter: function (val) {
            return parseInt(val);
          },
          offsetY: -20,
          style: {
            fontSize: '14px',
            colors: ["#304758"]
          }
        },
        stroke: {
          width: 0
        },
        series: [{
          name: 'Applications',
          data: result.tickets.count
        }],
        xaxis: {
          categories: result.tickets.date,
          position: 'bottom',
          labels: {
            offsetY: 0,
          },
          axisBorder: {
            show: true
          },
          axisTicks: {
            show: true
          }
        },
        tooltip: {
          enabled: true,
          theme: 'dark',
        },
        grid: {
          show: true,
          borderColor: 'rgba(66, 59, 116, 0.15)',
        },
        fill: {
          type: 'gradient',
          gradient: {
            shade: 'dark',
            gradientToColors: ['#08a50e'],
            shadeIntensity: 1,
            type: 'vertical',
            inverseColors: false,
            opacityFrom: 1,
            opacityTo: 1,
            stops: [0, 100, 100, 100]
          },
        },
        colors: ["#cddc35"],
        yaxis: {
          axisBorder: {
            show: false
          },
          axisTicks: {
            show: false,
          },
          labels: {
            show: false,
            formatter: function (val) {
              return parseInt(val);
            }
          }

        },
        responsive: [{
          breakpoint: 480,
          options: {
            chart: {
              height: 310
            },
            legend: {
              position: 'bottom'
            },
            title: {
              text: 'Monthly Application Submitions, 2018',
              floating: true,
              offsetY: 0,
              align: 'center',
              style: {
                fontSize: '13px',
                color: '#444'
              }
            }
          }
        }]
      }

      var chart = new ApexCharts(
        document.querySelector("#submitted-application"),
        options
      );
      chart.render();

      // chart 7
      var options = {
        chart: {
          height: 330,
          type: 'bar',
          toolbar: {
            show: false
          },
          dropShadow: {
            enabled: true,
            opacity: 0.1,
            blur: 3,
            left: -7,
            top: 22,
          }
        },
        plotOptions: {
          bar: {
            barHeight: '100%',
            endingShape: 'rounded',
            distributed: true,
            horizontal: true,
            dataLabels: {
              position: 'bottom'
            },
          }
        },
        fill: {
          type: 'gradient',
          gradient: {
            shade: 'dark',
            gradientToColors: ['#8f50ff', '#0072ff', '#f1076f', '#08a50e', '#f7971e', '#fc00ff', '#000428', '#ba8b02', '#009efd', '#000000'],
            shadeIntensity: 1,
            type: 'horizontal',
            opacityFrom: 1,
            opacityTo: 1,
            stops: [0, 100, 100, 100]
          },
        },
        colors: ['#d13adf', '#00c8ff', '#ff5447', '#cddc35', '#ffd200', '#00dbde', '#004e92', '#181818', '#2af598', '#ffffff'],
        dataLabels: {
          enabled: true,
          textAnchor: 'start',
          style: {
            colors: ['#fff']
          },
          formatter: function (val, opt) {
            return opt.w.globals.labels[opt.dataPointIndex] + ":  " + val
          },
          offsetX: 0,
          dropShadow: {
            enabled: true
          }
        },
        series: [{
          data: result.tickets_category.count,
        }],
        stroke: {
          width: 1,
          colors: ['#fff'],

        },
        xaxis: {
          categories: result.tickets_category.category,
        },
        yaxis: {
          labels: {
            show: false
          }
        },
        tooltip: {
          theme: 'dark',
          x: {
            show: false
          },
          y: {
            title: {
              formatter: function () {
                return ''
              }
            }
          }
        },
        grid: {
          show: true,
          borderColor: 'rgba(255, 255, 255, 0.12)',
        },
        legend: {
          show: false
        }
      }

      var chart = new ApexCharts(
        document.querySelector("#top-referrers"),
        options
      );

      chart.render();

      // chart 6

      var options = {
        chart: {
          height: 335,
          type: 'radialBar',
          toolbar: {
            show: false
          }
        },
        plotOptions: {
          radialBar: {
            startAngle: -135,
            endAngle: 225,
            hollow: {
              margin: 20,
              size: '80%',
              background: 'transparent',
              image: undefined,
              imageOffsetX: 0,
              imageOffsetY: 0,
              position: 'front',
              dropShadow: {
                enabled: true,
                top: 3,
                left: 0,
                blur: 4,
                opacity: 0.24
              }
            },
            track: {
              background: '#fff',
              //strokeWidth: '67%',
              margin: 0, // margin is in pixels
              dropShadow: {
                enabled: true,
                top: -3,
                left: 0,
                blur: 4,
                opacity: 0.35
              }
            },

            dataLabels: {
              showOn: 'always',
              name: {
                offsetY: -10,
                show: false,
                color: '#32393f',
                fontSize: '16px'
              },
              value: {
                formatter: function (val) {
                  return val + "%";
                },
                color: '#32393f',
                fontSize: '40px',
                show: true,
              }
            }
          }
        },
        fill: {
          type: 'gradient',
          gradient: {
            shade: 'light',
            type: 'horizontal',
            shadeIntensity: 0.5,
            gradientToColors: ['#f1076f'],
            inverseColors: false,
            opacityFrom: 1,
            opacityTo: 1,
            stops: [0, 100]
          }
        },
        // colors: ["#ff5447"],
        series: [result.tickets_total[1] / result.tickets_total[0] * 100],
        stroke: {
          lineCap: 'round'
        },
        labels: ['Median Ratio'],

      }

      var chart = new ApexCharts(
        document.querySelector("#vacancies-status"),
        options
      );

      $('#open-tickets').text(result.tickets_total[0])
      $('#closed-tickets').text(result.tickets_total[1])
      chart.render();
    }
  });

});