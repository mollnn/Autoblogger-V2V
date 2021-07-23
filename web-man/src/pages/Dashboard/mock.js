export default {
    bigStat: [{
            product: '视频收藏分布',
            total: '4,232',
            color: 'primary',
            registrations: {
                value: 830,
                profit: true,
            },
            bounce: {
                value: 4.5,
                profit: false,
            },
        },
        {
            product: '视频时间分布',
            total: '754',
            color: 'danger',
            registrations: {
                value: 30,
                profit: true,
            },
            bounce: {
                value: 2.5,
                profit: true,
            },
        },
        {
            product: '视频评论分布',
            total: '1,025',
            color: 'info',
            registrations: {
                value: 230,
                profit: true,
            },
            bounce: {
                value: 21.5,
                profit: false,
            },
        },
    ],
    table: [{
            id: 0,
            name: 'Mark Otto',
            email: 'ottoto@wxample.com',
            product: 'ON the Road',
            price: '$25 224.2',
            date: '11 May 2017',
            city: 'Otsego',
            status: 'Sent',
        },
        {
            id: 1,
            name: 'Jacob Thornton',
            email: 'thornton@wxample.com',
            product: 'HP Core i7',
            price: '$1 254.2',
            date: '4 Jun 2017',
            city: 'Fivepointville',
            status: 'Sent',
        },
        {
            id: 2,
            name: 'Larry the Bird',
            email: 'bird@wxample.com',
            product: 'Air Pro',
            price: '$1 570.0',
            date: '27 Aug 2017',
            city: 'Leadville North',
            status: 'Pending',
        },
        {
            id: 3,
            name: 'Joseph May',
            email: 'josephmay@wxample.com',
            product: 'Version Control',
            price: '$5 224.5',
            date: '19 Feb 2018',
            city: 'Seaforth',
            status: 'Declined',
        },
        {
            id: 4,
            name: 'Peter Horadnia',
            email: 'horadnia@wxample.com',
            product: 'Let\'s Dance',
            price: '$43 594.7',
            date: '1 Mar 2018',
            city: 'Hanoverton',
            status: 'Sent',
        },
    ],
};
import Highcharts from 'highcharts';
import config from '../../config';

const colors = config.app.colors;
const { inverse, info, primary, danger, warning, success, textColor } = colors;
const chartColors = config.app.chartColors;
const { axisColor } = chartColors;

let columnColors = [inverse, primary, info, success, warning, danger, '#EC2A00', '#FF8C22'];
let lineColors = [primary, success, warning];

export const chartData = {
    apex: {
        column: {
            series: [{
                data: [21, 22, 10, 28, 16, 21, 13, 30]
            }],
            options: {
                chart: {
                    height: 350,
                    type: 'bar',
                },
                colors: columnColors,
                plotOptions: {
                    bar: {
                        columnWidth: '45%',
                        distributed: true
                    }
                },
                dataLabels: {
                    enabled: false,
                },
                xaxis: {
                    categories: ['John', 'Joe', 'Jake', 'Amber', 'Peter', 'Mary', 'David', 'Lily'],
                    labels: {
                        style: {
                            colors: columnColors,
                            fontSize: '14px'
                        }
                    },
                    axisBorder: {
                        show: false
                    },
                    axisTicks: {
                        show: false
                    }
                },
                yaxis: {
                    labels: {
                        style: {
                            color: axisColor,
                        }
                    }
                },
            }
        },
        pie: {
            series: [25, 15, 44, 55, 41, 17],
            options: {
                labels: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                theme: {
                    monochrome: {
                        enabled: true,
                        color: primary,
                    }
                },
                stroke: {
                    show: false,
                    width: 0
                },
                legend: false,
                responsive: [{
                    breakpoint: 480,
                    options: {
                        chart: {
                            width: 200
                        },
                        legend: {
                            position: 'bottom'
                        }
                    }
                }]
            }
        }
    },
    echarts: {
        option09: {
            title: {
                text: '浏览器占比变化',
                subtext: '纯属虚构',
                top: 10,
                left: 10
            },
            tooltip: {
                trigger: 'item'
            },
            legend: {
                type: 'scroll',
                bottom: 10,
                data: (function() {
                    var list = [];
                    for (var i = 1; i <= 28; i++) {
                        list.push(i + 2000 + '');
                    }
                    return list;
                })()
            },
            visualMap: {
                top: 'middle',
                right: 10,
                color: ['red', 'yellow'],
                calculable: true
            },
            radar: {
                indicator: [
                    { text: 'IE8-', max: 400 },
                    { text: 'IE9+', max: 400 },
                    { text: 'Safari', max: 400 },
                    { text: 'Firefox', max: 400 },
                    { text: 'Chrome', max: 400 }
                ]
            },
            series: (function() {
                var series = [];
                for (var i = 1; i <= 28; i++) {
                    series.push({
                        name: '浏览器（数据纯属虚构）',
                        type: 'radar',
                        symbol: 'none',
                        lineStyle: {
                            width: 1
                        },
                        emphasis: {
                            areaStyle: {
                                color: 'rgba(0,250,0,0.3)'
                            }
                        },
                        data: [{
                            value: [
                                (40 - i) * 10,
                                (38 - i) * 4 + 60,
                                i * 5 + 10,
                                i * 9,
                                i * i / 2
                            ],
                            name: i + 2000 + ''
                        }]
                    });
                }
                return series;
            })()
        },
        option07: {
            title: [{
                    text: 'Michelson-Morley Experiment',
                    left: 'center'
                },
                {
                    text: 'upper: Q3 + 1.5 * IQR \nlower: Q1 - 1.5 * IQR',
                    borderColor: '#999',
                    borderWidth: 1,
                    textStyle: {
                        fontWeight: 'normal',
                        fontSize: 14,
                        lineHeight: 20
                    },
                    left: '10%',
                    top: '90%'
                }
            ],
            dataset: [{
                source: [
                    [850, 740, 900, 1070, 930, 850, 950, 980, 980, 880, 1000, 980, 930, 650, 760, 810, 1000, 1000, 960, 960],
                    [960, 940, 960, 940, 880, 800, 850, 880, 900, 840, 830, 790, 810, 880, 880, 830, 800, 790, 760, 800],
                    [880, 880, 880, 860, 720, 720, 620, 860, 970, 950, 880, 910, 850, 870, 840, 840, 850, 840, 840, 840],
                    [890, 810, 810, 820, 800, 770, 760, 740, 750, 760, 910, 920, 890, 860, 880, 720, 840, 850, 850, 780],
                    [890, 840, 780, 810, 760, 810, 790, 810, 820, 850, 870, 870, 810, 740, 810, 940, 950, 800, 810, 870]
                ]
            }, {
                transform: {
                    type: 'boxplot',
                    config: { itemNameFormatter: 'expr {value}' }
                }
            }, {
                fromDatasetIndex: 1,
                fromTransformResult: 1
            }],
            tooltip: {
                trigger: 'item',
                axisPointer: {
                    type: 'shadow'
                }
            },
            grid: {
                left: '10%',
                right: '10%',
                bottom: '15%'
            },
            xAxis: {
                type: 'category',
                boundaryGap: true,
                nameGap: 30,
                splitArea: {
                    show: false
                },
                splitLine: {
                    show: false
                }
            },
            yAxis: {
                type: 'value',
                name: 'km/s minus 299,000',
                splitArea: {
                    show: true
                }
            },
            series: [{
                    name: 'boxplot',
                    type: 'boxplot',
                    datasetIndex: 1
                },
                {
                    name: 'outlier',
                    type: 'scatter',
                    datasetIndex: 2
                }
            ]
        },
        option06: {
            tooltip: {},
            visualMap: {
                show: false,
                dimension: 2,
                min: -1,
                max: 1,
                inRange: {
                    color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
                }
            },
            xAxis3D: {},
            yAxis3D: {},
            zAxis3D: {},
            grid3D: {},
            series: [{
                type: 'surface',
                parametric: true,
                // shading: 'albedo',
                parametricEquation: {
                    u: {
                        min: -Math.PI,
                        max: Math.PI,
                        step: Math.PI / 20
                    },
                    v: {
                        min: 0,
                        max: Math.PI,
                        step: Math.PI / 20
                    },
                    x: function(u, v) {
                        return Math.sin(v) * Math.sin(u);
                    },
                    y: function(u, v) {
                        return Math.sin(v) * Math.cos(u);
                    },
                    z: function(u, v) {
                        return Math.cos(v);
                    }
                }
            }]
        },
        option05: {
            xAxis: {
                scale: true
            },
            yAxis: {
                scale: true
            },
            series: [{
                type: 'effectScatter',
                symbolSize: 20,
                data: [
                    [172.7, 105.2],
                    [153.4, 42]
                ]
            }, {
                type: 'scatter',
                data: [
                    [161.2, 51.6],
                    [167.5, 59.0],
                    [159.5, 49.2],
                    [157.0, 63.0],
                    [155.8, 53.6],
                    [170.0, 59.0],
                    [159.1, 47.6],
                    [166.0, 69.8],
                    [176.2, 66.8],
                    [160.2, 75.2],
                    [172.5, 55.2],
                    [170.9, 54.2],
                    [172.9, 62.5],
                    [153.4, 42.0],
                    [160.0, 50.0],
                    [147.2, 49.8],
                    [168.2, 49.2],
                    [175.0, 73.2],
                    [157.0, 47.8],
                    [167.6, 68.8],
                    [159.5, 50.6],
                    [175.0, 82.5],
                    [166.8, 57.2],
                    [176.5, 87.8],
                    [170.2, 72.8],
                    [174.0, 54.5],
                    [173.0, 59.8],
                    [179.9, 67.3],
                    [170.5, 67.8],
                    [160.0, 47.0],
                    [154.4, 46.2],
                    [162.0, 55.0],
                    [176.5, 83.0],
                    [160.0, 54.4],
                    [152.0, 45.8],
                    [162.1, 53.6],
                    [170.0, 73.2],
                    [160.2, 52.1],
                    [161.3, 67.9],
                    [166.4, 56.6],
                    [168.9, 62.3],
                    [163.8, 58.5],
                    [167.6, 54.5],
                    [160.0, 50.2],
                    [161.3, 60.3],
                    [167.6, 58.3],
                    [165.1, 56.2],
                    [160.0, 50.2],
                    [170.0, 72.9],
                    [157.5, 59.8],
                    [167.6, 61.0],
                    [160.7, 69.1],
                    [163.2, 55.9],
                    [152.4, 46.5],
                    [157.5, 54.3],
                    [168.3, 54.8],
                    [180.3, 60.7],
                    [165.5, 60.0],
                    [165.0, 62.0],
                    [164.5, 60.3],
                    [156.0, 52.7],
                    [160.0, 74.3],
                    [163.0, 62.0],
                    [165.7, 73.1],
                    [161.0, 80.0],
                    [162.0, 54.7],
                    [166.0, 53.2],
                    [174.0, 75.7],
                    [172.7, 61.1],
                    [167.6, 55.7],
                    [151.1, 48.7],
                    [164.5, 52.3],
                    [163.5, 50.0],
                    [152.0, 59.3],
                    [169.0, 62.5],
                    [164.0, 55.7],
                    [161.2, 54.8],
                    [155.0, 45.9],
                    [170.0, 70.6],
                    [176.2, 67.2],
                    [170.0, 69.4],
                    [162.5, 58.2],
                    [170.3, 64.8],
                    [164.1, 71.6],
                    [169.5, 52.8],
                    [163.2, 59.8],
                    [154.5, 49.0],
                    [159.8, 50.0],
                    [173.2, 69.2],
                    [170.0, 55.9],
                    [161.4, 63.4],
                    [169.0, 58.2],
                    [166.2, 58.6],
                    [159.4, 45.7],
                    [162.5, 52.2],
                    [159.0, 48.6],
                    [162.8, 57.8],
                    [159.0, 55.6],
                    [179.8, 66.8],
                    [162.9, 59.4],
                    [161.0, 53.6],
                    [151.1, 73.2],
                    [168.2, 53.4],
                    [168.9, 69.0],
                    [173.2, 58.4],
                    [171.8, 56.2],
                    [178.0, 70.6],
                    [164.3, 59.8],
                    [163.0, 72.0],
                    [168.5, 65.2],
                    [166.8, 56.6],
                    [172.7, 105.2],
                    [163.5, 51.8],
                    [169.4, 63.4],
                    [167.8, 59.0],
                    [159.5, 47.6],
                    [167.6, 63.0],
                    [161.2, 55.2],
                    [160.0, 45.0],
                    [163.2, 54.0],
                    [162.2, 50.2],
                    [161.3, 60.2],
                    [149.5, 44.8],
                    [157.5, 58.8],
                    [163.2, 56.4],
                    [172.7, 62.0],
                    [155.0, 49.2],
                    [156.5, 67.2],
                    [164.0, 53.8],
                    [160.9, 54.4],
                    [162.8, 58.0],
                    [167.0, 59.8],
                    [160.0, 54.8],
                    [160.0, 43.2],
                    [168.9, 60.5],
                    [158.2, 46.4],
                    [156.0, 64.4],
                    [160.0, 48.8],
                    [167.1, 62.2],
                    [158.0, 55.5],
                    [167.6, 57.8],
                    [156.0, 54.6],
                    [162.1, 59.2],
                    [173.4, 52.7],
                    [159.8, 53.2],
                    [170.5, 64.5],
                    [159.2, 51.8],
                    [157.5, 56.0],
                    [161.3, 63.6],
                    [162.6, 63.2],
                    [160.0, 59.5],
                    [168.9, 56.8],
                    [165.1, 64.1],
                    [162.6, 50.0],
                    [165.1, 72.3],
                    [166.4, 55.0],
                    [160.0, 55.9],
                    [152.4, 60.4],
                    [170.2, 69.1],
                    [162.6, 84.5],
                    [170.2, 55.9],
                    [158.8, 55.5],
                    [172.7, 69.5],
                    [167.6, 76.4],
                    [162.6, 61.4],
                    [167.6, 65.9],
                    [156.2, 58.6],
                    [175.2, 66.8],
                    [172.1, 56.6],
                    [162.6, 58.6],
                    [160.0, 55.9],
                    [165.1, 59.1],
                    [182.9, 81.8],
                    [166.4, 70.7],
                    [165.1, 56.8],
                    [177.8, 60.0],
                    [165.1, 58.2],
                    [175.3, 72.7],
                    [154.9, 54.1],
                    [158.8, 49.1],
                    [172.7, 75.9],
                    [168.9, 55.0],
                    [161.3, 57.3],
                    [167.6, 55.0],
                    [165.1, 65.5],
                    [175.3, 65.5],
                    [157.5, 48.6],
                    [163.8, 58.6],
                    [167.6, 63.6],
                    [165.1, 55.2],
                    [165.1, 62.7],
                    [168.9, 56.6],
                    [162.6, 53.9],
                    [164.5, 63.2],
                    [176.5, 73.6],
                    [168.9, 62.0],
                    [175.3, 63.6],
                    [159.4, 53.2],
                    [160.0, 53.4],
                    [170.2, 55.0],
                    [162.6, 70.5],
                    [167.6, 54.5],
                    [162.6, 54.5],
                    [160.7, 55.9],
                    [160.0, 59.0],
                    [157.5, 63.6],
                    [162.6, 54.5],
                    [152.4, 47.3],
                    [170.2, 67.7],
                    [165.1, 80.9],
                    [172.7, 70.5],
                    [165.1, 60.9],
                    [170.2, 63.6],
                    [170.2, 54.5],
                    [170.2, 59.1],
                    [161.3, 70.5],
                    [167.6, 52.7],
                    [167.6, 62.7],
                    [165.1, 86.3],
                    [162.6, 66.4],
                    [152.4, 67.3],
                    [168.9, 63.0],
                    [170.2, 73.6],
                    [175.2, 62.3],
                    [175.2, 57.7],
                    [160.0, 55.4],
                    [165.1, 104.1],
                    [174.0, 55.5],
                    [170.2, 77.3],
                    [160.0, 80.5],
                    [167.6, 64.5],
                    [167.6, 72.3],
                    [167.6, 61.4],
                    [154.9, 58.2],
                    [162.6, 81.8],
                    [175.3, 63.6],
                    [171.4, 53.4],
                    [157.5, 54.5],
                    [165.1, 53.6],
                    [160.0, 60.0],
                    [174.0, 73.6],
                    [162.6, 61.4],
                    [174.0, 55.5],
                    [162.6, 63.6],
                    [161.3, 60.9],
                    [156.2, 60.0],
                    [149.9, 46.8],
                    [169.5, 57.3],
                    [160.0, 64.1],
                    [175.3, 63.6],
                    [169.5, 67.3],
                    [160.0, 75.5],
                    [172.7, 68.2],
                    [162.6, 61.4],
                    [157.5, 76.8],
                    [176.5, 71.8],
                    [164.4, 55.5],
                    [160.7, 48.6],
                    [174.0, 66.4],
                    [163.8, 67.3]
                ],
            }]
        },
        option04: {
            legend: {
                top: 'bottom'
            },
            toolbox: {
                show: true,
                feature: {
                    mark: { show: true },
                    dataView: { show: true, readOnly: false },
                    restore: { show: true },
                    saveAsImage: { show: true }
                }
            },
            series: [{
                name: '面积模式',
                type: 'pie',
                radius: [50, 250],
                center: ['50%', '50%'],
                roseType: 'area',
                itemStyle: {
                    borderRadius: 8
                },
                data: [
                    { value: 40, name: 'rose 1' },
                    { value: 38, name: 'rose 2' },
                    { value: 32, name: 'rose 3' },
                    { value: 30, name: 'rose 4' },
                    { value: 28, name: 'rose 5' },
                    { value: 26, name: 'rose 6' },
                    { value: 22, name: 'rose 7' },
                    { value: 18, name: 'rose 8' }
                ]
            }]
        },
        option03: {
            xAxis: {
                type: 'category',
                data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                data: [820, 932, 901, 934, 1290, 1330, 1320],
                type: 'line',
                smooth: true
            }]
        },
        option02: {
            xAxis: {
                type: 'category',
                data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                data: [820, 932, 901, 934, 1290, 1330, 1320],
                type: 'line',
                smooth: true
            }]
        },
        option01: {
            xAxis: {
                type: 'category',
                data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                data: [820, 932, 901, 934, 1290, 1330, 1320],
                type: 'line',
                smooth: true
            }],
            grid: {
                x: 30,
                y: 10,
                x2: 5,
                height: 120,
                y2: 20,
                borderWidth: 15
            },
        },
        line: {
            color: lineColors,
            tooltip: {
                trigger: 'none',
                axisPointer: {
                    type: 'cross'
                }
            },
            legend: {
                data: ['2015 Precipitation', '2016 Precipitation'],
                textStyle: {
                    color: axisColor
                }
            },
            grid: {
                top: 70,
                bottom: 50,
            },
            xAxis: [{
                    type: 'category',
                    axisTick: {
                        alignWithLabel: true
                    },
                    axisLine: {
                        onZero: false,
                        lineStyle: {
                            color: lineColors[1]
                        }
                    },
                    axisPointer: {
                        label: {
                            formatter: function(params) {
                                return 'Precipitation  ' + params.value +
                                    (params.seriesData.length ? '：' + params.seriesData[0].data : '');
                            }
                        }
                    },
                    data: ["2016-1", "2016-2", "2016-3", "2016-4", "2016-5", "2016-6", "2016-7", "2016-8", "2016-9", "2016-10", "2016-11", "2016-12"]
                },
                {
                    type: 'category',
                    axisTick: {
                        alignWithLabel: true
                    },
                    axisLine: {
                        onZero: false,
                        lineStyle: {
                            color: lineColors[0]
                        }
                    },
                    axisPointer: {
                        label: {
                            formatter: function(params) {
                                return 'Precipitation  ' + params.value +
                                    (params.seriesData.length ? '：' + params.seriesData[0].data : '');
                            }
                        }
                    },
                    data: ["2015-1", "2015-2", "2015-3", "2015-4", "2015-5", "2015-6", "2015-7", "2015-8", "2015-9", "2015-10", "2015-11", "2015-12"]
                }
            ],
            yAxis: [{
                type: 'value',
                axisLabel: {
                    color: axisColor
                },
                axisLine: {
                    lineStyle: {
                        color: axisColor
                    }
                },
            }],
            series: [{
                    name: '2015 Precipitation',
                    type: 'line',
                    xAxisIndex: 1,
                    smooth: true,
                    data: [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
                },
                {
                    name: '2016 Precipitation',
                    type: 'line',
                    smooth: true,
                    data: [3.9, 5.9, 11.1, 18.7, 48.3, 69.2, 231.6, 46.6, 55.4, 18.4, 10.3, 0.7]
                }
            ]
        },
        donut00: {
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}: {c} ({d}%)"
            },
            legend: {
                show: false
            },
            color: [primary, success, danger, warning, info],
            series: [{
                name: 'Access source',
                type: 'pie',
                radius: ['50%', '70%'],
                avoidLabelOverlap: false,
                label: {
                    normal: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        show: true,
                        textStyle: {
                            fontSize: '30',
                            fontWeight: 'bold'
                        }
                    }
                },
                labelLine: {
                    normal: {
                        show: false
                    }
                },
                data: [
                    { value: 335, name: 'Direct interview' },
                    { value: 310, name: 'Email marketing' },
                    { value: 234, name: 'Alliance advertising' },
                    { value: 135, name: 'Video ad' },
                    { value: 1548, name: 'Search engine' }
                ]
            }]
        },
        river: {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'line',
                    lineStyle: {
                        color: 'rgba(0,0,0,0.2)',
                        width: 1,
                        type: 'solid'
                    }
                }
            },

            legend: {
                data: ['DQ', 'TY', 'SS', 'QG', 'SY', 'DD'],
                textStyle: {
                    color: axisColor
                }
            },
            color: [primary, success, warning, danger, info, inverse],
            singleAxis: {
                top: 50,
                bottom: 50,
                axisTick: {},
                axisLabel: {
                    color: axisColor
                },
                type: 'time',
                axisPointer: {
                    animation: true,
                    label: {
                        show: true
                    }
                },
                splitLine: {
                    show: true,
                    lineStyle: {
                        type: 'dashed',
                        opacity: 0.2
                    }
                },
                axisLine: {
                    lineStyle: {
                        color: axisColor
                    }
                },
            },

            series: [{
                type: 'themeRiver',
                itemStyle: {
                    emphasis: {
                        shadowBlur: 20,
                        shadowColor: 'rgba(0, 0, 0, 0.8)'
                    }
                },
                data: [
                    ['2015/11/08', 10, 'DQ'],
                    ['2015/11/09', 15, 'DQ'],
                    ['2015/11/10', 35, 'DQ'],
                    ['2015/11/11', 38, 'DQ'],
                    ['2015/11/12', 22, 'DQ'],
                    ['2015/11/13', 16, 'DQ'],
                    ['2015/11/14', 7, 'DQ'],
                    ['2015/11/15', 2, 'DQ'],
                    ['2015/11/16', 17, 'DQ'],
                    ['2015/11/17', 33, 'DQ'],
                    ['2015/11/18', 40, 'DQ'],
                    ['2015/11/19', 32, 'DQ'],
                    ['2015/11/20', 26, 'DQ'],
                    ['2015/11/21', 35, 'DQ'],
                    ['2015/11/22', 40, 'DQ'],
                    ['2015/11/23', 32, 'DQ'],
                    ['2015/11/24', 26, 'DQ'],
                    ['2015/11/25', 22, 'DQ'],
                    ['2015/11/26', 16, 'DQ'],
                    ['2015/11/27', 22, 'DQ'],
                    ['2015/11/28', 10, 'DQ'],
                    ['2015/11/08', 35, 'TY'],
                    ['2015/11/09', 36, 'TY'],
                    ['2015/11/10', 37, 'TY'],
                    ['2015/11/11', 22, 'TY'],
                    ['2015/11/12', 24, 'TY'],
                    ['2015/11/13', 26, 'TY'],
                    ['2015/11/14', 34, 'TY'],
                    ['2015/11/15', 21, 'TY'],
                    ['2015/11/16', 18, 'TY'],
                    ['2015/11/17', 45, 'TY'],
                    ['2015/11/18', 32, 'TY'],
                    ['2015/11/19', 35, 'TY'],
                    ['2015/11/20', 30, 'TY'],
                    ['2015/11/21', 28, 'TY'],
                    ['2015/11/22', 27, 'TY'],
                    ['2015/11/23', 26, 'TY'],
                    ['2015/11/24', 15, 'TY'],
                    ['2015/11/25', 30, 'TY'],
                    ['2015/11/26', 35, 'TY'],
                    ['2015/11/27', 42, 'TY'],
                    ['2015/11/28', 42, 'TY'],
                    ['2015/11/08', 21, 'SS'],
                    ['2015/11/09', 25, 'SS'],
                    ['2015/11/10', 27, 'SS'],
                    ['2015/11/11', 23, 'SS'],
                    ['2015/11/12', 24, 'SS'],
                    ['2015/11/13', 21, 'SS'],
                    ['2015/11/14', 35, 'SS'],
                    ['2015/11/15', 39, 'SS'],
                    ['2015/11/16', 40, 'SS'],
                    ['2015/11/17', 36, 'SS'],
                    ['2015/11/18', 33, 'SS'],
                    ['2015/11/19', 43, 'SS'],
                    ['2015/11/20', 40, 'SS'],
                    ['2015/11/21', 34, 'SS'],
                    ['2015/11/22', 28, 'SS'],
                    ['2015/11/23', 26, 'SS'],
                    ['2015/11/24', 37, 'SS'],
                    ['2015/11/25', 41, 'SS'],
                    ['2015/11/26', 46, 'SS'],
                    ['2015/11/27', 47, 'SS'],
                    ['2015/11/28', 41, 'SS'],
                    ['2015/11/08', 10, 'QG'],
                    ['2015/11/09', 15, 'QG'],
                    ['2015/11/10', 35, 'QG'],
                    ['2015/11/11', 38, 'QG'],
                    ['2015/11/12', 22, 'QG'],
                    ['2015/11/13', 16, 'QG'],
                    ['2015/11/14', 7, 'QG'],
                    ['2015/11/15', 2, 'QG'],
                    ['2015/11/16', 17, 'QG'],
                    ['2015/11/17', 33, 'QG'],
                    ['2015/11/18', 40, 'QG'],
                    ['2015/11/19', 32, 'QG'],
                    ['2015/11/20', 26, 'QG'],
                    ['2015/11/21', 35, 'QG'],
                    ['2015/11/22', 40, 'QG'],
                    ['2015/11/23', 32, 'QG'],
                    ['2015/11/24', 26, 'QG'],
                    ['2015/11/25', 22, 'QG'],
                    ['2015/11/26', 16, 'QG'],
                    ['2015/11/27', 22, 'QG'],
                    ['2015/11/28', 10, 'QG'],
                    ['2015/11/08', 10, 'SY'],
                    ['2015/11/09', 15, 'SY'],
                    ['2015/11/10', 35, 'SY'],
                    ['2015/11/11', 38, 'SY'],
                    ['2015/11/12', 22, 'SY'],
                    ['2015/11/13', 16, 'SY'],
                    ['2015/11/14', 7, 'SY'],
                    ['2015/11/15', 2, 'SY'],
                    ['2015/11/16', 17, 'SY'],
                    ['2015/11/17', 33, 'SY'],
                    ['2015/11/18', 40, 'SY'],
                    ['2015/11/19', 32, 'SY'],
                    ['2015/11/20', 26, 'SY'],
                    ['2015/11/21', 35, 'SY'],
                    ['2015/11/22', 4, 'SY'],
                    ['2015/11/23', 32, 'SY'],
                    ['2015/11/24', 26, 'SY'],
                    ['2015/11/25', 22, 'SY'],
                    ['2015/11/26', 16, 'SY'],
                    ['2015/11/27', 22, 'SY'],
                    ['2015/11/28', 10, 'SY'],
                    ['2015/11/08', 10, 'DD'],
                    ['2015/11/09', 15, 'DD'],
                    ['2015/11/10', 35, 'DD'],
                    ['2015/11/11', 38, 'DD'],
                    ['2015/11/12', 22, 'DD'],
                    ['2015/11/13', 16, 'DD'],
                    ['2015/11/14', 7, 'DD'],
                    ['2015/11/15', 2, 'DD'],
                    ['2015/11/16', 17, 'DD'],
                    ['2015/11/17', 33, 'DD'],
                    ['2015/11/18', 4, 'DD'],
                    ['2015/11/19', 32, 'DD'],
                    ['2015/11/20', 26, 'DD'],
                    ['2015/11/21', 35, 'DD'],
                    ['2015/11/22', 40, 'DD'],
                    ['2015/11/23', 32, 'DD'],
                    ['2015/11/24', 26, 'DD'],
                    ['2015/11/25', 22, 'DD'],
                    ['2015/11/26', 16, 'DD'],
                    ['2015/11/27', 22, 'DD'],
                    ['2015/11/28', 10, 'DD']
                ]
            }]
        }
    },
    highcharts: {
        mixed: {
            chart: {
                type: 'spline',
                height: 350
            },
            exporting: {
                enabled: false
            },
            title: {
                text: 'Snow depth at Vikjafjellet, Norway',
                style: {
                    color: textColor
                }
            },
            credits: {
                enabled: false
            },
            xAxis: {
                type: 'datetime',
                dateTimeLabelFormats: { // don't display the dummy year
                    month: '%e. %b',
                    year: '%b'
                },
                labels: {
                    style: {
                        color: axisColor
                    }
                }
            },
            yAxis: {
                min: 0,
                title: {
                    enabled: false
                },
                labels: {
                    style: {
                        color: axisColor
                    }
                },
            },
            tooltip: {
                headerFormat: '<b>{series.name}</b><br>',
                pointFormat: '{point.x:%e. %b}: {point.y:.2f} m'
            },
            legend: {
                enabled: false
            },
            plotOptions: {
                series: {
                    marker: {
                        enabled: false,
                        symbol: 'circle'
                    }
                }
            },
            colors: [success, warning, info],

            series: [{
                name: "Winter 2017-2018",
                data: [
                    [Date.UTC(1970, 10, 25), 0],
                    [Date.UTC(1970, 11, 6), 0.25],
                    [Date.UTC(1970, 11, 20), 1.41],
                    [Date.UTC(1970, 11, 25), 1.64],
                    [Date.UTC(1971, 0, 4), 1.6],
                    [Date.UTC(1971, 0, 17), 2.55],
                    [Date.UTC(1971, 0, 24), 2.62],
                    [Date.UTC(1971, 1, 4), 2.5],
                    [Date.UTC(1971, 1, 14), 2.42],
                    [Date.UTC(1971, 2, 6), 2.74],
                    [Date.UTC(1971, 2, 14), 2.62],
                    [Date.UTC(1971, 2, 24), 2.6],
                    [Date.UTC(1971, 3, 1), 2.81],
                    [Date.UTC(1971, 3, 11), 2.63],
                    [Date.UTC(1971, 3, 27), 2.77],
                    [Date.UTC(1971, 4, 4), 2.68],
                    [Date.UTC(1971, 4, 9), 2.56],
                    [Date.UTC(1971, 4, 14), 2.39],
                    [Date.UTC(1971, 4, 19), 2.3],
                    [Date.UTC(1971, 5, 4), 2],
                    [Date.UTC(1971, 5, 9), 1.85],
                    [Date.UTC(1971, 5, 14), 1.49],
                    [Date.UTC(1971, 5, 19), 1.27],
                    [Date.UTC(1971, 5, 24), 0.99],
                    [Date.UTC(1971, 5, 29), 0.67],
                    [Date.UTC(1971, 6, 3), 0.18],
                    [Date.UTC(1971, 6, 4), 0]
                ]
            }, {
                name: "Winter 2018-2019",
                type: 'areaspline',
                data: [
                    [Date.UTC(1970, 10, 9), 0],
                    [Date.UTC(1970, 10, 15), 0.23],
                    [Date.UTC(1970, 10, 20), 0.25],
                    [Date.UTC(1970, 10, 25), 0.23],
                    [Date.UTC(1970, 10, 30), 0.39],
                    [Date.UTC(1970, 11, 5), 0.41],
                    [Date.UTC(1970, 11, 10), 0.59],
                    [Date.UTC(1970, 11, 15), 0.73],
                    [Date.UTC(1970, 11, 20), 0.41],
                    [Date.UTC(1970, 11, 25), 1.07],
                    [Date.UTC(1970, 11, 30), 0.88],
                    [Date.UTC(1971, 0, 5), 0.85],
                    [Date.UTC(1971, 0, 11), 0.89],
                    [Date.UTC(1971, 0, 17), 1.04],
                    [Date.UTC(1971, 0, 20), 1.02],
                    [Date.UTC(1971, 0, 25), 1.03],
                    [Date.UTC(1971, 0, 30), 1.39],
                    [Date.UTC(1971, 1, 5), 1.77],
                    [Date.UTC(1971, 1, 26), 2.12],
                    [Date.UTC(1971, 3, 19), 2.1],
                    [Date.UTC(1971, 4, 9), 1.7],
                    [Date.UTC(1971, 4, 29), 0.85],
                    [Date.UTC(1971, 5, 7), 0]
                ]
            }, {
                name: "Winter 2019-2020",
                type: 'areaspline',
                data: [
                    [Date.UTC(1970, 9, 15), 0],
                    [Date.UTC(1970, 9, 31), 0.09],
                    [Date.UTC(1970, 10, 7), 0.17],
                    [Date.UTC(1970, 10, 10), 0.1],
                    [Date.UTC(1970, 11, 10), 0.1],
                    [Date.UTC(1970, 11, 13), 0.1],
                    [Date.UTC(1970, 11, 16), 0.11],
                    [Date.UTC(1970, 11, 19), 0.11],
                    [Date.UTC(1970, 11, 22), 0.08],
                    [Date.UTC(1970, 11, 25), 0.23],
                    [Date.UTC(1970, 11, 28), 0.37],
                    [Date.UTC(1971, 0, 16), 0.68],
                    [Date.UTC(1971, 0, 19), 0.55],
                    [Date.UTC(1971, 0, 22), 0.4],
                    [Date.UTC(1971, 0, 25), 0.4],
                    [Date.UTC(1971, 0, 28), 0.37],
                    [Date.UTC(1971, 0, 31), 0.43],
                    [Date.UTC(1971, 1, 4), 0.42],
                    [Date.UTC(1971, 1, 7), 0.39],
                    [Date.UTC(1971, 1, 10), 0.39],
                    [Date.UTC(1971, 1, 13), 0.39],
                    [Date.UTC(1971, 1, 16), 0.39],
                    [Date.UTC(1971, 1, 19), 0.35],
                    [Date.UTC(1971, 1, 22), 0.45],
                    [Date.UTC(1971, 1, 25), 0.62],
                    [Date.UTC(1971, 1, 28), 0.68],
                    [Date.UTC(1971, 2, 4), 0.68],
                    [Date.UTC(1971, 2, 7), 0.65],
                    [Date.UTC(1971, 2, 10), 0.65],
                    [Date.UTC(1971, 2, 13), 0.75],
                    [Date.UTC(1971, 2, 16), 0.86],
                    [Date.UTC(1971, 2, 19), 1.14],
                    [Date.UTC(1971, 2, 22), 1.2],
                    [Date.UTC(1971, 2, 25), 1.27],
                    [Date.UTC(1971, 2, 27), 1.12],
                    [Date.UTC(1971, 2, 30), 0.98],
                    [Date.UTC(1971, 3, 3), 0.85],
                    [Date.UTC(1971, 3, 6), 1.04],
                    [Date.UTC(1971, 3, 9), 0.92],
                    [Date.UTC(1971, 3, 12), 0.96],
                    [Date.UTC(1971, 3, 15), 0.94],
                    [Date.UTC(1971, 3, 18), 0.99],
                    [Date.UTC(1971, 3, 21), 0.96],
                    [Date.UTC(1971, 3, 24), 1.15],
                    [Date.UTC(1971, 3, 27), 1.18],
                    [Date.UTC(1971, 3, 30), 1.12],
                    [Date.UTC(1971, 4, 3), 1.06],
                    [Date.UTC(1971, 4, 6), 0.96],
                    [Date.UTC(1971, 4, 9), 0.87],
                    [Date.UTC(1971, 4, 12), 0.88],
                    [Date.UTC(1971, 4, 15), 0.79],
                    [Date.UTC(1971, 4, 18), 0.54],
                    [Date.UTC(1971, 4, 21), 0.34],
                    [Date.UTC(1971, 4, 25), 0]
                ]
            }]
        },
    }
};

export let liveChartInterval = null;

export const liveChart = {
    liveChartInterval: null,
    colors: ['#D4688C'],
    chart: {
        height: 250,
        type: 'spline',
        animation: Highcharts.svg, // don't animate in old IE
        marginRight: 10,
        events: {
            load: function() {

                // set up the updating of the chart each second
                var series = this.series[0];
                liveChartInterval = setInterval(function() {
                    var x = (new Date()).getTime(), // current time
                        y = 31415926 + 114514 * Math.random();
                    series.addPoint([x, y], true, true);
                }, 1000);
            }
        }
    },

    time: {
        useUTC: false
    },
    credits: {
        enabled: false
    },
    title: false,
    xAxis: {
        type: 'datetime',
        tickPixelInterval: 150,
        labels: {
            style: {
                color: axisColor
            }
        },
        lineWidth: 0,
        tickWidth: 0
    },
    yAxis: {
        title: {
            enabled: false
        },
        plotLines: [{
            value: 0,
            width: 1,
            color: axisColor
        }],
        labels: {
            style: {
                color: axisColor
            }
        }
    },
    tooltip: {
        headerFormat: '<b>{series.name}</b><br/>',
        pointFormat: '{point.x:%Y-%m-%d %H:%M:%S}<br/>{point.y:.2f}'
    },
    legend: {
        enabled: false
    },
    exporting: {
        enabled: false
    },
    series: [{
        name: '在线用户人数',
        data: (function() {
            // generate an array of random data
            var data = [],
                time = (new Date()).getTime(),
                i;

            for (i = -19; i <= 0; i += 1) {
                data.push({
                    x: time + i * 1000,
                    y: 31415926 + 114514 * Math.random()
                });
            }
            return data;
        }())
    }]
};