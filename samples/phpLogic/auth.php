<?php

include 'utils.php';

error_reporting(E_ALL);
ini_set("log_errors", true);
ini_set("error_log", "/errorlog.log");



//$streamkey = $argv[1];
$streamkey = $_POST["name"];

error_log(print_r($streamkey, true));

if (!$streamkey){
    echo "\nNo streamkey\n";
    DenyAccess();
}


$tableName = 'dynamo7539873d-dev';
$eav = $marshaler->marshalJson('
    {
        ":pk": "' . $streamkey . '"
    }
');

$params = [
    'TableName' => $tableName,
    'KeyConditionExpression' => '#pk = :pk',
    'ExpressionAttributeNames'=> [ '#pk' => 'pk' ],
    'ExpressionAttributeValues'=> $eav
];

try {
    $result = $dynamodb->query($params);

    if (!$result ['Items']){
        denyAccess();
    }
    foreach ($result['Items'] as $destination) {
        if ($marshaler->unmarshalValue($destination['service']) == 'primary' && !($marshaler->unmarshalValue($destination['active']))){
            denyAccess();
        }
    }

    allowAccess();

} catch (DynamoDbException $e){
    echo "Unable to query:\n";
    denyAccess();
}

?>