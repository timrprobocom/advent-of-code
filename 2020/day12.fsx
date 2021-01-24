open System.IO

type Position = int * int

type Direction = North | East | South | West

type Instruction =
  /// Advance a number of steps
  | Advance of int
  /// Rotate 90 degrees clockwise
  | Rotate
  /// Advance steps in this direction
  | AdvanceIn of int * Direction

/// Retrieve a list of instructions from the given input string.
let parseInstruction (instruction: string): Instruction list =
  match instruction.[0], int (instruction.Substring(1)) with
  | 'F', steps -> [Advance steps]
  // `R180` would result in [Rotate; Rotate]
  | 'R', degrees -> List.replicate (degrees / 90) Rotate
  // `L90` would result in [Rotate; Rotate; Rotate]
  | 'L', degrees -> List.replicate ((360 - degrees) / 90) Rotate
  | 'N', steps -> [AdvanceIn (steps, North)]
  | 'E', steps -> [AdvanceIn (steps, East)]
  | 'W', steps -> [AdvanceIn (steps, West)]
  | 'S', steps -> [AdvanceIn (steps, South)]

/// Retrieve a new position by moving `n` steps in a given direction from a given position
let move (n: int) (direction: Direction) ((x, y): Position): Position =
  match direction with
  | North -> (x, y + n)
  | East -> (x + n, y)
  | South -> (x, y - n)
  | West -> (x - n, y)

/// Retrieve a new direction by rotating 90 degrees clockwise from a given direction
let rotate (direction: Direction): Direction =
  match direction with
  | North -> East
  | East -> South
  | South -> West
  | West -> North

type State = Position * Direction

/// Retrieve a new state by applying the given instruction to the given state
let eval ((position, direction): State) (instruction: Instruction): State =
  match instruction with
  // When advancing, the position changes and the direction stays the same
  | Advance steps -> (position |> move steps direction), direction
  | AdvanceIn (steps, thisdirection) -> (position |> move steps thisdirection), direction
  // When rotating, the position stays the same and the direction changes
  | Rotate -> position, (direction |> rotate)
let initialState: State = (0, 0), East

let mandist (((x,y),dir): State): int =
  abs(x) + abs(y)

let finalState =
  File.ReadAllLines("day12.txt")
  |> Seq.collect parseInstruction
  |> Seq.fold eval initialState

printfn "Final state: %A" finalState
printfn "Part 1: %A" (finalState |> mandist)
// With the example input this would print "Final state: ((3, -10), East)"
