#!/usr/bin/env bash
mkdir /tmp/learners
gunicorn backend:app --worker-class gevent --bind unix:/tmp/learners/learners.sock
