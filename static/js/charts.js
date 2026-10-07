function createRadarChart(canvasId, models) {
    // Normalizzazione dei valori
    const maxValues = {
        accuracy: 1,
        loss: 1,
        execution_time: Math.max(models.centralized.kpi.execution_time, models.federated.kpi.execution_time),
        memory_usage: Math.max(models.centralized.kpi.memory_usage, models.federated.kpi.memory_usage),
        instruction_count: Math.max(models.centralized.kpi.instruction_count, models.federated.kpi.instruction_count)
    };

    // Conversione dei valori in percentuali
    const normalizedCentralized = {
        accuracy: models.centralized.kpi.accuracy * 100,
        loss: models.centralized.kpi.loss * 100,
        execution_time: (models.centralized.kpi.execution_time / maxValues.execution_time) * 100,
        memory_usage: (models.centralized.kpi.memory_usage / maxValues.memory_usage) * 100,
        instruction_count: (models.centralized.kpi.instruction_count / maxValues.instruction_count) * 100
    };

    const normalizedFederated = {
        accuracy: models.federated.kpi.accuracy * 100,
        loss: models.federated.kpi.loss * 100,
        execution_time: (models.federated.kpi.execution_time / maxValues.execution_time) * 100,
        memory_usage: (models.federated.kpi.memory_usage / maxValues.memory_usage) * 100,
        instruction_count: (models.federated.kpi.instruction_count / maxValues.instruction_count) * 100
    };

    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Accuracy', 'Execution Time', 'Memory Usage', 'Loss', 'Instruction Count'],
            datasets: [
                {
                    label: 'Centralized Model (CNN)',
                    data: [
                        normalizedCentralized.accuracy,
                        normalizedCentralized.execution_time,
                        normalizedCentralized.memory_usage,
                        normalizedCentralized.loss,
                        normalizedCentralized.instruction_count
                    ],
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgb(54, 162, 235)',
                    pointBackgroundColor: 'rgb(54, 162, 235)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(54, 162, 235)'
                },
                {
                    label: 'Federated Model (FedAvg)',
                    data: [
                        normalizedFederated.accuracy,
                        normalizedFederated.execution_time,
                        normalizedFederated.memory_usage,
                        normalizedFederated.loss,
                        normalizedFederated.instruction_count
                    ],
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgb(255, 99, 132)',
                    pointBackgroundColor: 'rgb(255, 99, 132)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(255, 99, 132)'
                }
            ]
        },
        options: {
            plugins: {
                legend: {
                    labels: {
                        // enlarge legend text without changing other sizes
                        font: {
                            size: 14
                        }
                    }
                }
            },
            elements: {
                line: {
                    borderWidth: 3
                }
            },
            scales: {
                r: {
                    angleLines: {
                        display: true
                    },
                    suggestedMin: 0,
                    suggestedMax: 100,
                    // enlarge only the radial point labels (the labels around the radar)
                    pointLabels: {
                        font: {
                            size: 16
                        },
                        color: '#333'
                    },
                    ticks: {
                        display: true,
                        stepSize: 20,
                        color: '#666'
                    }
                }
            }
        }
    });
}

function createGaugeChart(containerId, value, maxValue, label) {
    const ctx = document.getElementById(containerId).getContext('2d');
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [value, maxValue - value],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(54, 162, 235, 0.2)'
                ]
            }]
        },
        options: {
            circumference: 180,
            rotation: -90,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: label
                }
            }
        }
    });
}


function createBarChart(canvasId, models) {
    // Normalizzazione dei valori per renderli comparabili
    const maxValues = {
        accuracy: 1,
        loss: 1,
        execution_time: Math.max(models.centralized.kpi.execution_time, models.federated.kpi.execution_time),
        memory_usage: Math.max(models.centralized.kpi.memory_usage, models.federated.kpi.memory_usage),
        instruction_count: Math.max(models.centralized.kpi.instruction_count, models.federated.kpi.instruction_count)
    };

    // Normalizzazione dei valori per il grafico a barre
    const normalizedCentralized = {
        accuracy: models.centralized.kpi.accuracy * 100,
        loss: models.centralized.kpi.loss * 100,
        execution_time: (models.centralized.kpi.execution_time / maxValues.execution_time) * 100,
        memory_usage: (models.centralized.kpi.memory_usage / maxValues.memory_usage) * 100,
        instruction_count: (models.centralized.kpi.instruction_count / maxValues.instruction_count) * 100
    };

    const normalizedFederated = {
        accuracy: models.federated.kpi.accuracy * 100,
        loss: models.federated.kpi.loss * 100,
        execution_time: (models.federated.kpi.execution_time / maxValues.execution_time) * 100,
        memory_usage: (models.federated.kpi.memory_usage / maxValues.memory_usage) * 100,
        instruction_count: (models.federated.kpi.instruction_count / maxValues.instruction_count) * 100
    };

    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Accuracy', 'Loss', 
                'Execution Time', 'Memory Usage', 'Instruction Count'],
            datasets: [
                {
                    label: 'Centralized Model (CNN)',
                    data: [
                        normalizedCentralized.accuracy,
                        normalizedCentralized.loss,
                        normalizedCentralized.execution_time,
                        normalizedCentralized.memory_usage,
                        normalizedCentralized.instruction_count
                    ],
                    backgroundColor: 'rgba(54, 162, 235, 0.8)',
                    borderColor: 'rgb(54, 162, 235)',
                    borderWidth: 1
                },
                {
                    label: 'Federated Model (FedAvg)',
                    data: [
                        normalizedFederated.accuracy,
                        normalizedFederated.loss,
                        normalizedFederated.execution_time,
                        normalizedFederated.memory_usage,
                        normalizedFederated.instruction_count
                    ],
                    backgroundColor: 'rgba(255, 99, 132, 0.8)',
                    borderColor: 'rgb(255, 99, 132)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Normalized Value(%)'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Comparing Metrics Between Models'
                }
            }
        }
    });
}


function createLineChart(canvasId, models) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['0%', '25%', '50%', '75%', '100%'],
            datasets: [
                {
                    label: 'Centralized Model (CNN)',
                    data: [0, 25, 50, 75, models.centralized.kpi.accuracy * 100],
                    borderColor: 'rgb(54, 162, 235)',
                    tension: 0.1
                },
                {
                    label: 'Federated Model (FedAvg)',
                    data: [0, 20, 45, 70, models.federated.kpi.accuracy * 100],
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}