var app=angular.module('myApp', []);

      app.config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');
      });

     app.controller("myCtrl", ["$scope","$http", function($scope,$http)
     {
        var user,emp,emp_filter_a,selectedIndex,edit_user,user_items;
        $scope.emp_filter_a='';
        $scope.emp = [];
        $scope.user={};
        $scope.selectedIndex=0;
        $scope.edit_user={};
        $scope.login_info={};
        $scope.edit_profile={};
        $scope.profile = {};
        $scope.pages = [1];
        $scope.offset_value = 0;
        $scope.role = '';

          $scope.addUser=function()
            {
                $http.post('/add',{'user_data':$scope.user}).then(function(response)
                {
                $scope.get_user($scope.offset_value);
                $scope.paginate()
//                  $scope.emp.push($scope.user);
//                  $scope.user={};
//                  localStorage.setItem('user_items', JSON.stringify(this.emp));
                });
             }

            $scope.editUser=function(x,index)
            {
                $scope.edit_user=angular.copy(x);
                $scope.selectedIndex=index;
            }

            $scope.saveEditUser=function()
            {
                $scope.emp[$scope.selectedIndex]=$scope.edit_user;
                $http.post('/edit_user',{'user_edit':$scope.edit_user, 'user_id':$scope.edit_user.id}).then(function(response)
                  {
//                        $scope.edit_user = response.emp_edit
                  });
//                localStorage.setItem('user_items', JSON.stringify(this.emp));
            }

           $scope.remove= function(index)
            {
                $http.post('/delete_user',{'del_id':$scope.emp[index].id}).then(function(response)
                {
                    $scope.emp.splice(index,1);
                    $scope.paginate()
                });
    //                localStorage.setItem('user_items', JSON.stringify(this.emp));
            }

             $scope.get_user=function(off_index)
            {
                $scope.offset_value=off_index*5
                $http.post('/get_user',{'offset_value':$scope.offset_value}).then(function(response)
                {
                    $scope.emp=response.data.emp_data;
                    $scope.user={};
                });
            }

            $scope.get_user($scope.offset_value)

            $scope.column = "id";
            $scope.reverse = false;

            $scope.sort=function(col)
            {
                if ($scope.column ==  col)
                {$scope.reverse = !$scope.reverse}
                else
                {$scope.reverse = false}
                $scope.column = col;
            }

            $scope.getSort=function(col)
            {
                if ($scope.column == col)
                {
                    if  ($scope.reverse)
                    {
                    return 'far fa-arrow-alt-circle-down'
                    }
                    else
                    {return 'far fa-arrow-alt-circle-up'}
                }
                else
                return '';
            }

            $scope.getProfile=function()
            {
                $http.post('/profile_user').then(function(response)
                {
                    $scope.edit_profile = $scope.profile
                    $scope.profile['uname']=response.data.profile_uname;
                    $scope.profile['psw']=response.data.profile_psw;
                    $scope.profile['email']=response.data.profile_email;
                });
            }

            $scope.paginate=function()
            {
                $http.post('/total_records').then(function(response)
                {
                    $scope.role = response.data.role
                    console.log($scope.role)
                    $scope.pg = response.data.pg
                    if ($scope.pg in $scope.pages)
                        return
                    else
                        $scope.pages.push($scope.pg)
                });
            }

            $scope.paginate()


                $scope.salary_insight = function()
                {
                    // Get data
                    $http.post('/get_id').then(function(response)
                    {
                        $scope.chart_name = response.data.name;
                        $scope.chart_salary = response.data.salary
                        $scope.plot_chart();
                    });

                }
                $scope.plot_chart = function(){
                    var salaryChart = (document.getElementById('main'));
                    var salaryCharts =echarts.init(salaryChart);
//                    echarts.dispose = echarts.init(salaryChart)

                    var option =
                    {
                        color: ['#3398DB'],
                        title : {
                            text : 'SALARY INSIGHT'
                        },

                        tooltip : {
                            show : true,
                            trigger : 'axis'
                        },

                        xAxis : {
                            type : 'category',
                            splitLine : false,
                            data : $scope.chart_name
                        },

                        yAxis : {
                            type : 'value',
                            splitLine : false
                        },

                        series : [{
                            type : 'bar',
                            barWidth : '50%',
                            data : $scope.chart_salary
                        }]
                    };

                    if(option && typeof option == 'object')
                    {salaryCharts.setOption(option);}
                }
        }]);
