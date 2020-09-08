<?php
require 'vendor/autoload.php';

// AWS SDK
date_default_timezone_set('UTC');
use Aws\DynamoDb\Exception\DynamoDbException;
use Aws\DynamoDb\Marshaler;

$sdk = new Aws\Sdk([
    'region'   => 'eu-west-1',
    'version'  => 'latest'
]);

$dynamodb = $sdk->createDynamoDb();
$marshaler = new Marshaler();



// FUNCTIONS
function denyAccess() {
    echo "Denied";
    http_response_code(403);
    exit();
};

function allowAccess() {
    echo "Allow";
    http_response_code(403);
    exit();
};

?>