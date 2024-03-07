(function(){
    var myChart = echarts.init(document.querySelector(".line .chart"));
    option = {
        color:['#91cc75', '#fac858'],
        tooltip: {
          trigger: 'axis'
        },
        legend: {
            textStyle:{
              color:"#4c9bfd"
            },
            
        },
        grid: {
            top:'20%',
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true,
            show:true,
            borderColor:'#012f4a',
            
          },
        toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: false },
            
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
          axisLabel: {
            
            color:"#4c9bfd"
          }
          
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: '{value} °C',
            color:"#4c9bfd"
          },
          splitLine:{
            lineStyle:{
              color:'#012f4a'
            }
          }
          
        },
        series: [
          {
            name: '最高气温',
            type: 'line',
            data: [10, 11, 13, 11, 12, 12, 9],
            markPoint: {
              data: [
                { type: 'max', name: 'Max' },
                { type: 'min', name: 'Min' }
              ]
            },
            
            
          },
          {
            name: '最低气温',
            type: 'line',
            data: [1, -2, 2, 5, 3, 2, 0],
            markPoint: {
              data: [
                { type: 'max', name: 'Max' },
                { type: 'min', name: 'Min' }
              ]
            },
            
          }
        ]
      };
      myChart.setOption(option);
})();