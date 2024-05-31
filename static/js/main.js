//const coursesList = {{ courses | safe }}
//const resultsList = {{ results | safe }};
const ctx = document.getElementById('barchart');

  const barchart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: coursesList,
      datasets: [{
        label: '# of Votes',
        data: resultsList,
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });

  const ctx11 = document.getElementById('barchart11');

  new Chart(ctx11, {
      type: 'doughnut',
      data : {
        labels: [
          'Red',
          'Blue',
          'Yellow'
        ],
        datasets: [{
          label: 'My First Dataset',
          data: [300, 50, 100],
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)'
          ],
          hoverOffset: 4
        }]
      }
    }

  );


 /* const ctx2 = document.getElementById('barchart2');

  new Chart(ctx2, {
    type: 'bar',
    data: {
      labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
      datasets: [{
        label: '# of Votes',
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
  */

var ctx2 = document.getElementById('barchart2').getContext('2d');
var dataValues = [12, 19, 3, 5];
var dataLabels = [0, 1, 2, 3, 4];

var myChart = new Chart(ctx2, {
  type: 'bar',
  data: {
    labels: dataLabels,
    datasets: [{
      label: 'Group A',
      data: dataValues,
      backgroundColor: 'rgba(255, 99, 132, 1)',
      /*backgroundColor: 'rgba(255, 99, 132, 0.5)',
      borderColor: 'rgba(255, 99, 132, 1)',*/
      barPercentage: 1.25
    }]
  },
  options: {
    scales: {
      x: [{
        display: false,
        barPercentage: 1.3, // Définition de la valeur de barPercentage
        ticks: {
          max: 3
        }
      }, {
        display: true,
        ticks: {
          autoSkip: false,
          max: 4,
        }
      }],
      y: [{
        ticks: {
          beginAtZero: true
        }
      }]
    }
  }
});

var ctx3 = document.getElementById('barchart3').getContext('2d');

// Données pour le diagramme en boîte
/* var data = {
  datasets: [{
    label: 'Box Plot',
    data: [{
      min: 10,
      q1: 15,
      median: 20,
      q3: 25,
      max: 30
    }]
  }]
};

// Options du diagramme en boîte
var options = {
  scales: {
    x: {
      type: 'category',
      labels: ['Data']
    }
  }
};

// Créer le diagramme en boîte
var boxPlot = new Chart(ctx2, {
  type: 'boxplot',
  data: data,
  options: options
});

*/document.addEventListener('DOMContentLoaded', () => {
      // Générer des données aléatoires pour le diagramme de dispersion
      var data = {
        datasets: [{
          label: 'Points Evaluation 1',
          data: generateData(),
          backgroundColor: 'rgba(255, 99, 132, 0.5)', // Couleur de remplissage des points
          borderColor: 'rgba(255, 99, 132, 1)', // Couleur du contour des points
          borderWidth: 1 // Largeur du contour des points
        }, {
          label: 'Points Evaluation 2',
          data: generateData(),
          backgroundColor: 'rgba(54, 162, 235, 0.5)', // Couleur de remplissage des points
          borderColor: 'rgba(54, 162, 235, 1)', // Couleur du contour des points
          borderWidth: 1 // Largeur du contour des points
        }]
      };

      // Options du diagramme de dispersion
      var options = {
        scales: {
          x: {
            type: 'linear',
            position: 'bottom' // Position de l'axe des x
          },
          y: {
            type: 'linear',
            position: 'left' // Position de l'axe des y
          }
        }
      };

      // Obtenez le contexte du canvas


      // Créer le diagramme de dispersion
      var scatterChart = new Chart(ctx3
      , {
        type: 'scatter',
        data: data,
        options: options
      });

      // Fonction pour générer des données aléatoires
      function generateData() {
        return Array.from({ length: 10 }, () => ({
          x: Math.random() * 50,
          y: Math.random() * 50
        }));
      }
    });


   const data2 = {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      datasets: [{
        label: 'Weekly Sales',
        outlierColor: '#999999',
        padding:0,
        itemRadius: 0,
        //data: [18, 12, 6, 9, 12, 3, 9],
        data: [
        randomValue(100, 0, 100), // min wisker
        randomValue(100, 0, 20), // lower Quartille
        randomValue(100, 20, 70), // Media
        randomValue(100, 60, 100), // Inter Quartile range (IQR)
        randomValue(40, 50, 100), // Mean
        randomValue(100, 60, 120), // upper quartile
        randomValue(100, 80, 100), // max whisker
        ],
        backgroundColor:'rgba(255, 26, 104, 0.2)',
        borderColor: 'rgba(255, 26, 104, 1)',
        borderWidth: 1,
      }]
    };

    // config
    const config2 = {
      type: 'boxplot',
      data: data2,
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    };

    // render init block
    const myChart2 = new Chart(
      document.getElementById('barchart1'),
      config2
    );

    function randomValue(count, min, max){
        const delta = max - min;
        return Array.from({length: count}).map(() => Math.random() * delta + min);
    }

    // Instantly assign Chart.js version
    // const chartVersion = document.getElementById('barchart1');
    // chartVersion.innerText = Chart.version;

