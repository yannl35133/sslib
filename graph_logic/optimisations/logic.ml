open Containers

module IntSet = Set.Make (Int)

let ei_pp fmt = Fmt.pf fmt "EXTENDED_ITEM(%d)"

module Inventory = struct
  type inventory = IntSet.t * Z.t
  type t = inventory
  let empty_int = Z.zero
  let empty = IntSet.empty, empty_int
  let singleton n = IntSet.singleton n, Z.(one lsl n)

  let compare (_, n) (_, m) = Z.compare n m

  let (<=) : inventory -> inventory -> bool = fun (_, n) (_, m) -> Z.( Compare.( (n lor m) = m ))

  let union : inventory -> inventory -> inventory = fun (s, n) (t, m) -> IntSet.union s t, Z.( m lor n )

  let mem : int -> inventory -> bool = fun n (m, _) -> IntSet.mem n m

  let fold : _ -> inventory -> _ = fun f (s, _) -> IntSet.fold f s

  let pp : inventory CCSet.printer = fun fmt (s, _) -> Fmt.pf fmt "Inventory(%a)" (if IntSet.is_empty s then Fmt.nop else Fmt.braces @@ IntSet.pp ei_pp) s

  let of_list l : inventory = IntSet.of_list l, List.fold_left Z.(lor) Z.zero @@ List.map (fun n -> Z.(one lsl n)) l
end
type inventory = Inventory.inventory

module DNFInventory = struct
  type dnfinv = inventory list

  let empty : dnfinv = []

  let add inv dnf : dnfinv =
    let add = ref true in
    let dnf' = List.filter (fun inv' -> if Inventory.(inv <= inv') then false else (if Inventory.(inv' <= inv) then add := false; true)) dnf in
    if !add then inv :: dnf' else dnf'

  let remove_item item : dnfinv -> dnfinv =
    let mask = Inventory.singleton item in
    List.filter (fun inv -> not Inventory.(mask <= inv))
  let cmpt = ref (-1)
  let pp : dnfinv CCSet.printer =
    fun fmt s -> Fmt.pf fmt "DNFInventory(%a)" (* (incr cmpt; !cmpt) *) (if List.is_empty s then Fmt.nop else Fmt.braces @@ List.pp Inventory.pp) s

  let of_list = List.fold_left (Fun.flip add) empty
  let of_list2 l : dnfinv = l |> List.map Inventory.of_list |> List.fold_left (Fun.flip add) empty

  let fold : _ -> 'a -> dnfinv -> 'a = List.fold_left


  let rec lst_dnf_product f acc pre_args = function
    | hd :: tl ->
      (fun f -> List.fold_left f acc hd) @@ fun a i -> lst_dnf_product f a (i :: pre_args) tl
    | [] -> f acc pre_args
  let lst_dnf_product f acc l = lst_dnf_product f acc [] l

  let and_simplify =
    lst_dnf_product (fun new_req lst -> add (List.fold_left Inventory.union Inventory.empty lst) new_req)


end
type dnfinv = DNFInventory.dnfinv

let read_inv ((`List l) : Yojson.Safe.t) =
  l |> List.map (function (`Int i) -> i | _ -> assert false) |> Inventory.of_list

let read_dnf ((`List l) : Yojson.Safe.t) =
  l |> List.map read_inv |> DNFInventory.of_list

let read_requirements ((`List l) : Yojson.Safe.t) =
  l |> List.map (function `List l -> read_dnf (`List l) | `Assoc _ -> DNFInventory.empty | _ -> assert false) |> Array.of_list,
  l |> List.map (function `List _ -> false | `Assoc _ -> true | _ -> assert false) |> Array.of_list

let read_opaque ((`List l) : Yojson.Safe.t) =
  l |> List.map (function (`Int b) -> b <> 0 | _ -> assert false) |> Array.of_list


let pp : dnfinv option array CCArray.printer =
  Fmt.brackets @@ Array.pp @@ (fun pp fmt -> function Some req -> pp fmt req | None -> Fmt.pf fmt "None") @@ DNFInventory.pp


let print_if = let counter = ref 0 in fun () -> incr counter; !counter mod 99997 = 0

module IntMap = Map.Make (Int)

module CONSTANTS = struct
  let practice_sword = 437
  let beetle = 443
  let pouch = 453
  let high_rupee_farm = 470
  let empty_bottle = 473
  let one_pack = 480
  let sword = 500
  let clawshots = 65
  let bomb_bag = 62
  let lmf_back_exit = 2002
  let lmf_entrance_desert = 1709
  let last_macro = 520

end

let opaque_additions =
  let open CONSTANTS in
  let (--$) from length = List.init (length+1) ((+) from) in
  let distance_activator = sword+4 :: sword+7 --$ 2 in
  let sword_ = sword :: sword+2 :: sword+5 --$ 15 in
  let beetle_ = sword+3 :: distance_activator in
  let bomb_bag_ = sword+2 :: sword+5 :: sword+7 :: sword+8 :: sword+9 :: sword+12 :: sword+17 :: [] in
  let clawshots_ = sword+6 :: distance_activator in
  IntMap.of_list
  [
    (practice_sword, (sword_, None));
    (practice_sword + 1, (practice_sword --$ 1 @ sword_, None));
    (practice_sword + 2, (practice_sword --$ 2 @ sword_, None));
    (practice_sword + 3, (practice_sword --$ 3 @ sword_, None));
    (practice_sword + 4, (practice_sword --$ 4 @ sword_, None));
    (beetle, (beetle_, None));
    (beetle + 1, (beetle --$ 1 @ beetle_, None));
    (beetle + 2, (beetle --$ 2 @ beetle_, None));
    (beetle + 3, (beetle + 3 :: beetle --$ 1 @ beetle_, None));
    (beetle + 4, (beetle --$ 4 @ beetle_, None));
    (clawshots, (clawshots_, None));
    (bomb_bag, (bomb_bag_, None));
    (one_pack + 1, (one_pack --$ 1, None));
    (one_pack + 2, (one_pack --$ 2, None));
    (one_pack + 3, (one_pack --$ 3, None));
    (one_pack + 4, (one_pack --$ 4, None));
    (one_pack + 5, (one_pack --$ 5, None));
    (one_pack + 6, (one_pack --$ 6, None));
    (one_pack + 7, (one_pack --$ 7, None));
    (one_pack + 8, (one_pack --$ 8, None));
    (one_pack + 9, (one_pack --$ 9, None));
    (one_pack + 10, (one_pack --$ 10, None));
    (one_pack + 11, (one_pack --$ 11, None));
    (lmf_back_exit, ([lmf_back_exit], Some lmf_entrance_desert));
  ]

let deep_simplify reqs opaques =
  let len = Array.length reqs in
  let simplified = Array.make len false in
  let todo = Stack.of_seq Seq.(0 --^ len) in

  let rec simplify visited item : dnfinv * IntSet.t =
    let hit_a_visited = IntSet.empty in
    if IntSet.mem item visited then
      DNFInventory.of_list2 [[item]], IntSet.singleton item
    else if opaques.(item) then
      match IntMap.find_opt item opaque_additions with None -> DNFInventory.of_list2 [[item]], IntSet.empty
      | Some (add, None) -> DNFInventory.of_list2 [item :: add], IntSet.empty
      | Some (add, Some req_item) ->
          let visited = IntSet.add item visited in
          let item_req, h_a_v = simplify visited req_item in
          let req = DNFInventory.and_simplify DNFInventory.empty [DNFInventory.of_list2 [item :: add]; DNFInventory.remove_item item item_req] in
          req, IntSet.remove item (IntSet.union hit_a_visited h_a_v)
    else if simplified.(item) then
      reqs.(item), IntSet.empty
    else
      let visited = IntSet.add item visited in
      if print_if() then Fmt.pr "%d (stack size %d)@." item (Stack.length todo);
      let new_req, hit_a_visited =
      (fun f -> DNFInventory.fold f (DNFInventory.empty, hit_a_visited) reqs.(item)) @@ (fun (new_req, hit_a_visited) possibility ->
        let conj, hit_a_visited =
          (fun f -> Inventory.fold f possibility ([], hit_a_visited)) @@ (fun req_item (new_conj, hit_a_visited) ->
            let item_req, h_a_v = simplify visited req_item in
            (* if print_if() then Fmt.pr "%d: %a in %d: %a@." req_item DNFInventory.pp item_req item DNFInventory.pp new_req; *)
            let hit_a_visited = IntSet.union hit_a_visited h_a_v in
            DNFInventory.remove_item item item_req :: new_conj, hit_a_visited)
        in
        DNFInventory.and_simplify new_req conj, hit_a_visited)
      in
      let hit_a_visited = IntSet.remove item hit_a_visited in
      if List.length new_req <= 2 then reqs.(item) <- new_req;
      (* if print_if() then Fmt.pr "%d: %a@." item DNFInventory.pp new_req; *)

      if IntSet.is_empty hit_a_visited then begin
        Fmt.pr "%d: %a@." item DNFInventory.pp new_req;
        reqs.(item) <- new_req;
        simplified.(item) <- true
      end else if Stack.length todo < 3000 then Stack.push item todo;

      new_req, hit_a_visited
  in
  while not(Stack.is_empty todo) do
    simplify IntSet.empty (let item = Stack.pop todo in Fmt.pr ">%d (stack size %d)@." item (Stack.length todo); item) |> ignore
  done

let erase_additions reqs =
  let len = Array.length reqs in
  for i = 0 to len -1 do
    reqs.(i) <- Fun.flip List.map reqs.(i) (fun inv ->
      (fun f -> IntMap.fold f opaque_additions inv) (fun i (m, _) inv ->
        if Inventory.mem i inv then
          let (s, _) = inv in
          let l = IntSet.to_list s in
          let l' = List.filter (fun i' -> not (List.mem i' m)) l in
          Inventory.of_list (i :: l')
        else
          inv
      )
    )
  done

let (* main *) () =
  let t = Yojson.Safe.from_file "requirements.json" in
  let reqs, opaque = read_requirements t in
  let opaque2 = Array.copy opaque in
  for i = 0 to CONSTANTS.last_macro do opaque2.(i) <- true done;
  deep_simplify reqs opaque2;
  (* Fmt.pr "STEP 2 : -----------------------@.";
  let () =
  let open CONSTANTS in
  for i = practice_sword to practice_sword + 5 do opaque.(i) <- true done;
  for i = beetle to beetle + 3 do opaque.(i) <- true done;
  opaque.(pouch) <- true; opaque.(high_rupee_farm) <- true; opaque.(empty_bottle) <- true;
  for i = one_pack to one_pack + 12 do opaque.(i) <- true done;
  in
  deep_simplify reqs opaque; *)
  erase_additions reqs;
  let reqs_opt = Array.map2 (fun b r -> if not b then Some r else None) opaque reqs in
  (* DNFInventory.cmpt := -1; *)
  let c = open_out "requirements_out.txt" in
  let f = Format.of_chan c in
  Fmt.pf f "%a@." pp reqs_opt;
  close_out c
