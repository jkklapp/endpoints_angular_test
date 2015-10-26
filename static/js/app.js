var app = angular.module('testapp', []);

app.controller('GreetingsController', ['$http', function($http) {

	this.greetings = [];

	this.message = "";

	var that = this;

	//this has to be acquired from an auth API endpoint
	this.token = 'secret';

	$http.get('/_ah/api/helloworld/v1/hellogreeting').success(function(data) {
		that.greetings = data["items"];
	});

	this.addAnonGreeting = function() {
		$http({
			method: "POST",
			url: '/_ah/api/helloworld/v1/hellogreeting/authed',
		 	data: {'message': this.message}
		}).success(that.callback);
	};

	this.addAuthedGreeting = function() {
		var token = this.token;
	  $http({
			method: "POST",
			url: '/_ah/api/helloworld/v1/hellogreeting/authed?access_token='+token,
			data: {'message': this.message},
			headers: {'Authorization': 'Bearer '+token}
		}).success(that.callback);
	};

	this.callback = function(data) {
		that.greetings.push(data);
		that.message = "";
	};

}]);
