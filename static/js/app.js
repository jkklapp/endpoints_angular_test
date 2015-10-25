var app = angular.module('testapp', []);

app.controller('GreetingsController', ['$http', function($http) {

	this.greetings = [];

	this.message = "";

	var that = this;

	$http.get('/_ah/api/helloworld/v1/hellogreeting').success(function(data) {
		that.greetings = data["items"];
	});

	this.addGreeting = function() {
		//this.greetings.push(this.greetingText);
		$http.post('/_ah/api/helloworld/v1/hellogreeting/authed', {'message': this.message}).success(function(data) {
			that.greetings.push(data);
			that.message = "";
		});
	};

}]);