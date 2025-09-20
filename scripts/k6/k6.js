import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
    stages: [
        { duration: '30s', target: 10 },   // ramp up to 10 users
        { duration: '1m', target: 50 },    // stay at 50 users
        { duration: '30s', target: 0 },    // ramp down to 0 users
    ],
};

export default function () {
    http.get('http://127.0.0.1:8001/process');
    sleep(1);
}