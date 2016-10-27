Array.prototype.getItem = function(key, value) {
    for (var i=0; i < this.length; i++) {
        if (this[i][key] === value) {
            return this[i];
        }
    }
}

Array.prototype.setItem = function(key, value, new_value) {
    for (var i=0; i < this.length; i++) {
        if (this[i][key] === value) {
            this[i] = new_value;
            return;
        }
    }
}