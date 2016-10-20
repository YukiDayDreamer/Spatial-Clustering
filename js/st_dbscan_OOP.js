var STDBSCAN = function (X, eps1, eps2, MinPts) {
    this.X = X;
    this.len = X.length;
    this.eps1 = eps1;
    this.eps2 = eps2;
    this.MinPts = MinPts;

    // spatial distance
    this.sp_dist = function (a, b) {
        return Math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]));
    };
    // temporal distance
    this.tp_dist = function (a, b) {
        return Math.abs(a[2] - b[2]);
    };
    // retrieve list of neighbors
    this.retrieve_neighbors = function (point) {
        var neighbors = []; // list of neighbor
        for (var iter = 0; iter < this.len; iter++) {
            var dist1 = this.sp_dist(point, this.X[iter]);
            var dist2 = this.tp_dist(point, this.X[iter]);
            if (dist1 <= this.eps1 && dist2 <= this.eps2) {
                neighbors.push(iter);
            }
        }
        return neighbors;
    };
    // main function entry
    this.run = function () {
        var cluster_label = 0; // label meaning: 0:unmarked; 1,2,3,...:cluster label; "noise":noise
        var labels = new Array(this.len).fill(0); // new an 0 array to store labels
        var clusters = []; // final output

        // clustering data points
        for (var i = 0; i < this.len; i++) {
            var neighbors = this.retrieve_neighbors(X[i]);
            if (neighbors.length < this.MinPts) {
                // if it is unmarked, mark it "noise"
                if (labels[i] === 0) {
                    labels[i] = "noise";
                }
            } else {
                cluster_label += 1; // construct a new cluster
                var cluster = []; // construct cluster

                // mark label for all unmarked neighbors
                for (var j1 = 0; j1 < neighbors.length; j1++) {
                    // if no other labels
                    if (labels[neighbors[j1]] === 0 || labels[neighbors[j1]] === "noise") {
                        labels[neighbors[j1]] = cluster_label;
                        cluster.push(neighbors[j1]);
                    }
                }

                // check the sub-circle of all objects
                while (neighbors.length !== 0) {
                    var j2;
                    j2 = neighbors.pop();
                    var sub_neighbors = this.retrieve_neighbors(X[j2]);
                    // mark all unmarked neighbors
                    if (sub_neighbors.length >= this.MinPts) {
                        for (var k = 0; k < sub_neighbors.length; k++) {
                            // if no other labels 
                            if (labels[sub_neighbors[k]] === 0 || labels[sub_neighbors[k]] === "noise") {
                                // might include |cluster_avg() - X[index]| < delta_eps
                                neighbors.push(sub_neighbors[k]);
                                labels[sub_neighbors[k]] = cluster_label;
                                cluster.push(sub_neighbors[k]);
                            }
                        }
                    }
                }

                // remove cluster of small size
                if (cluster.length < this.MinPts) {
                    for (var j3 = 0; j3 < this.len; j3++) {
                        if (labels[j3] === cluster_label) {
                            labels[j3] = "noise";
                        }
                    }
                } else {
                    clusters.push(cluster);
                }
            }
        }

        //console.log(clusters);
        return clusters;
    };
};


// test data
/* para1 : spatial coordinate x
 * para2 : spatial coordinate y
 * para3 : time stamp t
 */
        
var X = [
    [10.0001, 10.0001, 1], [10.0002, 10.0002, 2], [10.0003, 10.0003, 3], [10.0004, 10.0004, 4],
    [20.0001, 20.0001, 1], [20.0002, 20.0002, 2], [20.0003, 20.0003, 3], [20.0004, 20.0004, 4],
    [30.0001, 30.0001, 1], [30.0002, 30.0002, 2], [30.0003, 30.0003, 3], [30.0004, 30.0004, 4],
    [40.0001, 40.0001, 1], [40.0002, 40.0002, 2], [40.0003, 40.0003, 3], [40.0004, 40.0004, 4],
    [70, 70, 1],
    [80, 80, 2]
];
var eps1 = 100;
var eps2 = 5;
var MinPts = 4;

var st_dbscan = new STDBSCAN(X, eps1, eps2, MinPts);
var result = st_dbscan.run();
