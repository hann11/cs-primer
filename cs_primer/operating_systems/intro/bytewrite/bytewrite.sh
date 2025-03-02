printf '' > tmp

blocks=$(stat -f %b tmp)


for i in {1..10000}; do
    printf 'a' >> tmp
    block_new=$(stat -f %b tmp)
    size=$(stat -f %z tmp)
    if [ $block_new -gt $blocks ]; then
        echo "Block increased from $blocks to $block_new at $size bytes"
        blocks=$block_new
    fi
done