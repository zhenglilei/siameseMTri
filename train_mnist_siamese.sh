#!/usr/bin/env sh

TOOLS=./build/tools

$TOOLS/caffe train --solver=examples/siameseMTri/mnist_siamese_solver.prototxt
