<?php

declare(strict_types=1);

header('Content-Type: application/json');

function response(array $data, int $status = 200): void
{
    http_response_code($status);

    echo json_encode(
        $data,
        JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT
    );

    exit;
}

$method = $_SERVER['REQUEST_METHOD'];

$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

if ($method === 'GET' && $uri === '/') {
    response([
        'message' => 'DevOps Pipeline Example'
    ]);
}

if ($method === 'GET' && $uri === '/health') {
    response([
        'status' => 'ok'
    ]);
}

if ($method === 'GET' && $uri === '/users') {
    response([
        [
            'id' => 1,
            'name' => 'José'
        ],
        [
            'id' => 2,
            'name' => 'Maria'
        ]
    ]);
}

if ($method === 'GET' && preg_match('#^/users/(\d+)$#', $uri, $matches)) {
    response([
        'id' => (int) $matches[1],
        'name' => 'José'
    ]);
}

if ($method === 'POST' && $uri === '/users') {

    $body = json_decode(
        file_get_contents('php://input'),
        true
    );

    if (!is_array($body)) {
        response([
            'error' => 'Invalid JSON'
        ], 400);
    }

    $errors = [];

    if (!isset($body['id']) || $body['id'] === '') {
        $errors['id'] = 'Id is required';
    }

    if (!isset($body['name']) || trim($body['name']) === '') {
        $errors['name'] = 'Name is required';
    }

    if (!empty($errors)) {
        response([
            'errors' => $errors
        ], 400);
    }

    response([
        'message' => 'User created successfully',
        'user' => [
            'id' => (int) $body['id'],
            'name' => trim($body['name'])
        ]
    ], 201);
}

if ($method === 'GET' && $uri === '/error') {
    response([
        'error' => 'Internal Server Error'
    ], 500);
}

response([
    'error' => 'Not Found'
], 404);