var socket = io.connect(
    'http://' + document.domain + ':' + location.port + '/chat');

console.log('connected');

var app = angular.module('ticketApp', []);

app.factory('socket', function ($rootScope) {
    var socket = io.connect('/chat');
    return {
        on: function (eventName, callback) {
            socket.on(eventName, function () {
                var args = arguments;
                $rootScope.$apply(function () {
                    callback.apply(socket, args);
                });
            });
        },
        emit: function (eventName, data, callback) {
            socket.emit(eventName, data, function () {
                var args = arguments;
                $rootScope.$apply(function () {
                    if (callback) {
                        callback.apply(socket, args);
                    }
                });
            })
        }
    };
});

app.controller('TicketListController',
        ['$scope', '$http', 'socket', function($scope, $http, socket) {
            $scope.tickets = [];
            $scope.ticketStatuses = [];

            $http.get('/api/ticketstatus/list')
                .success(function(data) {
                    $scope.ticketStatuses = data.ticketStatusNames;
                });

            function loadTickets(ticketStatus) {
                console.log('loading ' + ticketStatus + ' tickets');
                $http.get('/api/tickets/list/' + ticketStatus)
                    .success(function(data, status) {
                        $scope.tickets = data.records;
                    })
                    .error(function(data, status) {
                        console.log(JSON.stringify(data));
                    });
            }

            $scope.sendAdminMessage = function(ticketId) {
                var ticketLi = document.getElementById(
                        'ticket-list-item-' + ticketId);
                var user = $(ticketLi).find('.tl-email').text().trim();
                var msgContent = $(ticketLi).find('option:selected').val();
                socket.emit('admin message', {
                    data: msgContent,
                    destination: user
                });

                return false;
            }

            socket.on('server message', function(msg) {
                console.log(JSON.stringify(msg));
            });

            socket.on('error message', function(msg) {
                console.log(msg);
            });

            socket.on('new ticket', function(msg) {
                $http.get('/api/tickets/get/' + msg.ticketId, function(data) {
                    $scope.tickets.unshift(data);
                });
            });

            socket.emit('admin auth', { password: password });

            loadTickets('all');
        }]);
