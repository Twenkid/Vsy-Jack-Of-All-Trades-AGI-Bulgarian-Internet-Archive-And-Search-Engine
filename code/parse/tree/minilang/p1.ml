// Global constants and variables
//2.2026
const MAX_SIZE: int = 100;
var current_count: int = 0;

struct Point {
    x: int;
    y: int;
}

struct Player {
    pos: Point;
    id: int;
    is_active: bool;
}

fn calculate_distance(p1: Point, p2: Point) -> int {
    var dx: int = p2.x - p1.x;
    var dy: int = p2.y - p1.y;
    
    // Testing precedence: * and / before +
    return dx * dx + dy * dy;
}

fn main() -> void {
    var player1: Player = Player {
        pos: Point { x: 10, y: 20 },
        id: 1,
        is_active: true,
    };

    var i: int = 0;
    while (i < MAX_SIZE) {
        if (i % 2 == 0) {
            current_count = current_count + 1;
        } else {
            // Bitwise/Boolean NOT test
            var skip: bool = ~false;
        }
        i = i + 1;
    }
}	
