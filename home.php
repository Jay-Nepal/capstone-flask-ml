<div class="container-fluid">
    <div class="d-sm-flex justify-content-between align-items-center mb-4">
        <h3 class="text-dark mb-0">&nbsp;</h3><a class="btn btn-primary btn-sm d-none d-sm-inline-block" role="button" href="#"><i class="fas fa-download fa-sm text-white-50"></i> Generate Report</a>
    </div>
    <div class="row">
        <a href="mainpage.php?module=form&page=data_entry_table">
            <div class="col-md-6 col-xl-3 mb-4">
                <div class="card shadow border-start-primary py-2">
                    <div class="card-body">
                        <div class="row align-items-center no-gutters">
                            <div class="col me-2">
                                <div class="text-uppercase text-primary fw-bold text-xs mb-1"><span>Data Entry</span></div>
                                <div class="text-dark fw-bold h5 mb-0"><span>10</span></div>
                            </div>
                            <div class="col-auto"><i class="fas fa-calendar fa-2x text-gray-300"></i></div>
                        </div>
                    </div>
                </div>
            </div>
        </a>
        <div class="col-md-6 col-xl-3 mb-4">
            <div class="card shadow border-start-success py-2">
                <div class="card-body">
                    <div class="row align-items-center no-gutters">
                        <div class="col me-2">
                            <div class="text-uppercase text-success fw-bold text-xs mb-1"><span>Report</span></div>
                            <div class="text-dark fw-bold h5 mb-0"><span>12</span></div>
                        </div>
                        <div class="col-auto"><i class="fas fa-dollar-sign fa-2x text-gray-300"></i></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6 col-xl-3 mb-4">
            <div class="card shadow border-start-info py-2">
                <div class="card-body">
                    <div class="row align-items-center no-gutters">
                        <div class="col me-2">
                            <div class="text-uppercase text-info fw-bold text-xs mb-1"><span>Tasks</span></div>
                            <div class="row g-0 align-items-center">
                                <div class="col-auto">
                                    <div class="text-dark fw-bold h5 mb-0 me-3"><span>50%</span></div>
                                </div>
                                <div class="col">
                                    <div class="progress progress-sm">
                                        <div class="progress-bar bg-info" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width: 50%;"><span class="visually-hidden">50%</span></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-auto"><i class="fas fa-clipboard-list fa-2x text-gray-300"></i></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6 col-xl-3 mb-4">
            <div class="card shadow border-start-warning py-2">
                <div class="card-body">
                    <div class="row align-items-center no-gutters">
                        <div class="col me-2">
                            <div class="text-uppercase text-warning fw-bold text-xs mb-1"><span>Pending Requests</span></div>
                            <div class="text-dark fw-bold h5 mb-0"><span>18</span></div>
                        </div>
                        <div class="col-auto"><i class="fas fa-comments fa-2x text-gray-300"></i></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="col" >
            <canvas id="myChart"></canvas>
        </div>
        <div class="col" >
            <canvas id="myChart2"></canvas>
        </div>
    </div>
</div>
<?php
    // the easiest way to do it but this cost a lot of resources. can change to looping and array.
    $data_jan = 0;
    $data_feb = 1;
    $data_mac = 3;
    $data_apr = 4;
    $data_may = 5;
    $data_jun = 6;
    $data_jul = 7;
    $data_aug = 8;
    $data_sep = 9;
    $data_oct = 10;
    $data_nov = 11;
    $data_dec = 12;

    $data_by_month = $db->data_chart_by_month();
    $data_month = array();
    foreach($data_by_month as $key => $dtbm){
        $data_month[$key] = $dtbm;
    }

    $statuses = $db->invoice_status();
    $st = array();
    foreach($statuses as $s => $stt){
        $st[$s] = $stt;
    }

    $status_inv = $db->data_chart_by_status();
    $data_status = array();
    foreach($status_inv as $bil => $dcbs){
        $data_status[$bil] = $dcbs;
    }

     //print_r($data_status);
    echo $data_status['No']
    // print_r($db->data_chart_by_status());


?>

<script>
const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Jan','Feb','Mac','April','May','June','Jul','Aug','Sep','Oct','Nov','Dec'],
        datasets: [{
            label: 'PO Amount by Month',
            data: [<?php echo $data_month[1];?>,<?php echo $data_month[2];?>,<?php echo $data_month[3];?>,
            <?php echo $data_month[4];?>,<?php echo $data_month[5];?>,<?php echo $data_month[6];?>,
            <?php echo $data_month[7];?>,<?php echo $data_month[8];?>,<?php echo $data_month[9];?>,
            <?php echo $data_month[10];?>,<?php echo $data_month[11];?>,<?php echo $data_month[12];?>],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
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

const ctx2 = document.getElementById('myChart2').getContext('2d');
const myChart2 = new Chart(ctx2, {
    type: 'bar',
    data: {
        labels: ['<?php echo $st[0];?>','<?php echo $st[1];?>','<?php echo $st[2];?>'],
        datasets: [{
            label: 'PO Amount by Invoice Status',
            data: [<?php echo $data_status[$st[0]];?>, <?php echo $data_status[$st[1]];?>, <?php echo $data_status[$st[2]];?>],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
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
</script>
