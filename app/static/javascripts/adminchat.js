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
            $scope.chat = {};

            $http.get('/api/ticketstatus/list')
                .success(function(data) {
                    $scope.ticketStatuses = data.ticketStatusNames;
                });

            function loadTickets(ticketStatus) {
                console.log('loading ' + ticketStatus + ' tickets');
                $http.get('/api/tickets/list/' + ticketStatus)
                    .success(function(data, status) {
                        $scope.tickets = data.records;
                        for(var i = 0; i < $scope.tickets.length; i++) {
                            $scope.chat[$scope.tickets[i].ticketId] = [];
                        }
                    })
                    .error(function(data, status) {
                        console.log(JSON.stringify(data));
                    });
            }

            $scope.sendAdminMessage = function(ticketId) {
                var ticketLi = document.getElementById(
                        'ticket-list-item-' + ticketId);
                var msgContent = $(ticketLi).find('option:selected').val();
                socket.emit('admin message', {
                    data: msgContent,
                    destination: ticketId.toString()
                });

                return false;
            };

            $scope.sendChatMessage = function(ticketId) {
                var ticketLi = document.getElementById(
                        'ticket-list-item-' + ticketId);
                var msgContent = $(ticketLi).find('.chatinput > input[type="text"]').val();

                socket.emit('admin message', {
                    data: msgContent,
                    destination: ticketId.toString()
                });

                return false;
            };

            $scope.deleteTicket = function(ticketId) {
                $http.post('/api/tickets/delete/' + ticketId, {})
                    .success(function(data) {
                        for(var i = 0; i < $scope.tickets.length; i++) {
                            if($scope.tickets[i].ticketId === ticketId) {
                                $scope.tickets.splice(i, 1);
                                return;
                            }
                        }
                    });
            };

            $scope.updateTicket = function(ticketId) {
                var affectedTicket = null;
                for(var i = 0; i < $scope.tickets.length; i++) {
                    var ticket = $scope.tickets[i];
                    if(ticket.ticketId == ticketId) {
                        affectedTicket = ticket;
                        break;
                    }
                }

                $http.post('/api/tickets/modify/' + ticketId, {
                    ticketStatusName: affectedTicket.ticketStatusName
                }).success(function(data) {
                    console.log(JSON.stringify(data));
                });
            }

            socket.on('server message', function(msg) {
                console.log(JSON.stringify(msg));
            });

            socket.on('error message', function(msg) {
                console.log(msg);
            });

            socket.on('update ticket', function(msg) {
                for(var i = 0; i < $scope.tickets.length; i++) {
                    var ticket = $scope.tickets[i];
                    if(ticket.ticketId == msg.ticketId) {
                        ticket.ticketStatusName = msg.ticketStatusName;
                        console.log('updated ticket');
                        return;
                    }
                }
                console.log("ticket doesn't exist for update");
            });

            socket.on('new ticket', function(msg) {
                // the msg is the complete description of the ticket.
                console.log('new ticket');
                $scope.tickets.unshift(msg);
                $scope.chat[msg.ticketId] = [];
            });

            socket.on('delete ticket', function(msg) {
                for(var i = 0; i < $scope.tickets.length; i++) {
                    if($scope.tickets[i].ticketId == msg.ticketId) {
                        $scope.tickets.splice(i, 1);
                        return;
                    }
                }
            });

            socket.on('admin message', function(msg) {
                var dest = msg.destination;
                for(var i = 0; i < $scope.tickets.length; i++) {
                    var id = $scope.tickets[i].ticketId;
                    if(id == dest) {
                        if(typeof($scope.chat[id]) === 'undefined') {
                            $scope.chat[id] = []
                        }
                        $scope.chat[id].push({
                            sender: 'Operator',
                            type: 'admin-message',
                            data: msg.data
                        });
                        $('form.chatinput > input[type="text"]').val('');
                        return;
                    }
                }
            });

            socket.on('chat message', function(msg) {
                for(var i = 0; i < $scope.tickets.length; i++) {
                    var id = $scope.tickets[i].ticketId;
                    if(id == msg.sender) {
                        if(typeof($scope.chat[id]) === 'undefined') {
                            $scope.chat[id] = []
                        }
                        $scope.chat[id].push({
                            sender: $scope.tickets[i].userName,
                            type: 'message',
                            data: msg.data
                        });
                        console.log('got chat');
                        return;
                    }
                }
                console.log('got message from a ghost');
            });

            socket.emit('admin auth', { password: password });

            loadTickets('all');
        }
]);

