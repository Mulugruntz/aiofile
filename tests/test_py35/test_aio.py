from aiofile._aio import AIOFile
from aiofile.utils import Reader, Writer
from .. import *


@pytest.mark.asyncio
async def test_read(temp_file, uuid):
    with open(temp_file, "w") as f:
        f.write(uuid)

    aio_file = AIOFile(temp_file, 'r')

    data = await aio_file.read()
    data = data.decode()

    assert data == uuid


@pytest.mark.asyncio
async def test_read_write(temp_file, uuid):
    r_file = AIOFile(temp_file, 'r')
    w_file = AIOFile(temp_file, 'w')

    await w_file.write(uuid)
    await w_file.flush()

    data = await r_file.read()
    data = data.decode()

    assert data == uuid


@pytest.mark.asyncio
async def test_read_offset(temp_file, uuid):
    with open(temp_file, "w") as f:
        for _ in range(10):
            f.write(uuid)

    aio_file = AIOFile(temp_file, 'r')

    data = await aio_file.read(
        offset=len(uuid),
        size=len(uuid)
    )

    data = data.decode()

    assert data == uuid


@pytest.mark.asyncio
async def test_read_write_offset(temp_file, uuid):
    r_file = AIOFile(temp_file, 'r')
    w_file = AIOFile(temp_file, 'w')

    for i in range(10):
        await w_file.write(uuid, offset=i * len(uuid))

    await w_file.flush()

    data = await r_file.read(
        offset=len(uuid),
        size=len(uuid)
    )

    data = data.decode()

    assert data == uuid


@pytest.mark.asyncio
async def test_reader_writer(temp_file, uuid):
    r_file = AIOFile(temp_file, 'r')
    w_file = AIOFile(temp_file, 'w')

    writer = Writer(w_file)

    for _ in range(100):
        await writer(uuid)

    await w_file.flush()

    count = 0
    for async_chunk in Reader(r_file, chunk_size=len(uuid)):
        chunk = await async_chunk
        assert chunk.decode() == uuid
        count += 1

    assert count == 100

@pytest.mark.asyncio
async def test_reader_writer(loop, temp_file, uuid):
    r_file = AIOFile(temp_file, 'r')
    w_file = AIOFile(temp_file, 'w')

    writer = Writer(w_file)

    for _ in range(100):
        await writer(uuid)

    await w_file.flush()

    async for chunk in Reader(r_file, chunk_size=len(uuid)):
        assert chunk.decode() == uuid